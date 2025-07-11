import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis.asyncio as redis
from asgiref.sync import sync_to_async

REDIS_URL = "rediss://default:AazKAAIncDFhZDQ3OTA1ZjA3ODU0ZjQ5OTBkOGU2OTI4NzZjNjE3NHAxNDQyMzQ@vital-ladybird-44234.upstash.io:6379"

class FightQueue:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL, decode_responses=True)
        self.QUEUE_KEY = "fight_queue"
        self.NOME_HASH = "fight_nomes"
        self.CHANNEL_HASH = "fight_channels"

    async def debug_redis(self):
        fila = await self.redis.lrange(self.QUEUE_KEY, 0, -1)
        nomes = await self.redis.hgetall(self.NOME_HASH)
        canais = await self.redis.hgetall(self.CHANNEL_HASH)
        print(f"Fila: {fila}")
        print(f"Nomes: {nomes}")
        print(f"Canais: {canais}")

    async def add_to_queue(self, usuario_id, nome, channel_name):
        uid = str(usuario_id)
        # Evitar duplicata na fila
        fila_atual = await self.redis.lrange(self.QUEUE_KEY, 0, -1)
        if uid not in fila_atual:
            await self.redis.rpush(self.QUEUE_KEY, uid)
        await self.redis.hset(self.NOME_HASH, uid, nome)
        await self.redis.hset(self.CHANNEL_HASH, uid, channel_name)
        await self.debug_redis()

    async def remove_from_queue(self, usuario_id):
        uid = str(usuario_id)
        # Remover todas as ocorrências do usuário na fila para evitar duplicatas
        while True:
            removed = await self.redis.lrem(self.QUEUE_KEY, 0, uid)
            if removed == 0:
                break
        await self.redis.hdel(self.NOME_HASH, uid)
        await self.redis.hdel(self.CHANNEL_HASH, uid)

    async def get_current_queue(self):
        return await self.redis.lrange(self.QUEUE_KEY, 0, -1)

    async def pop_two_players(self):
        # Pega os dois primeiros jogadores da fila
        players = await self.redis.lrange(self.QUEUE_KEY, 0, 1)
        if len(players) < 2 or players[0] == players[1]:
            return None
        # Remove exatamente esses dois do começo da fila
        await self.redis.ltrim(self.QUEUE_KEY, 2, -1)
        return players

    async def get_nomes_by_ids(self, ids):
        if not ids:
            return []
        nomes = await self.redis.hmget(self.NOME_HASH, *ids)
        return [n if n else f"Desconhecido ({i})" for i, n in zip(ids, nomes)]

    async def get_channels_by_ids(self, ids):
        if not ids:
            return []
        canais = await self.redis.hmget(self.CHANNEL_HASH, *ids)
        return canais


class TestConsumer(AsyncWebsocketConsumer):
    queue = FightQueue()

    async def connect(self):
        self.usuario_id = await self.get_usuario_id_da_sessao()
        if not self.usuario_id:
            await self.close()
            return

        self.nome = await self.get_nome_usuario(self.usuario_id)

        await self.accept()

        # Remove canal antigo, se necessário
        canais_atuais = await self.queue.get_channels_by_ids([str(self.usuario_id)])
        if canais_atuais and canais_atuais[0] and canais_atuais[0] != self.channel_name:
            try:
                await self.channel_layer.group_discard("fila_pareamento", canais_atuais[0])
            except Exception:
                pass

        await self.queue.add_to_queue(self.usuario_id, self.nome, self.channel_name)
        await self.channel_layer.group_add("fila_pareamento", self.channel_name)
        await self.atualizar_fila_broadcast()

        players = await self.queue.pop_two_players()
        if players:
            self.room_name = f"fight_{players[0]}_{players[1]}"
            self.group_name = self.room_name

            # Adiciona os canais dos dois jogadores ao grupo da luta
            canais = await self.queue.get_channels_by_ids(players)
            for canal in canais:
                if canal:
                    await self.channel_layer.group_add(self.group_name, canal)

            # Garante que o canal atual esteja no grupo da luta
            if self.channel_name not in canais:
                await self.channel_layer.group_add(self.group_name, self.channel_name)

            nomes = await self.queue.get_nomes_by_ids(players)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "start.fight",
                    "players": nomes,
                    "group_name": self.group_name,
                    "message": "Jogo iniciado entre " + " e ".join(nomes),
                }
            )
        else:
            await self.send(json.dumps({"message": "Aguardando adversário..."}))


    async def disconnect(self, close_code):
        await self.queue.remove_from_queue(self.usuario_id)
        await self.channel_layer.group_discard("fila_pareamento", self.channel_name)
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.atualizar_fila_broadcast()

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data.get("message", "")
        print(f"Receive message: {msg} from user {self.usuario_id} group: {getattr(self, 'group_name', None)}")
        if hasattr(self, "group_name"):
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": msg,
                    "sender": str(self.usuario_id),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event.get("sender", "")
        }))

    async def start_fight(self, event):
        if not hasattr(self, "group_name") or not self.group_name:
            # define o nome do grupo a partir do nome do evento
            self.group_name = event.get("group_name")
            if self.group_name:
                await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "players": event["players"],
            "start": True
        }))

    async def fila_atualizada(self, event):
        await self.send(text_data=json.dumps({
            "queue": event["queue"]
        }))

    async def atualizar_fila_broadcast(self):
        fila_ids = await self.queue.get_current_queue()
        nomes = await self.queue.get_nomes_by_ids(fila_ids)
        await self.channel_layer.group_send(
            "fila_pareamento",
            {
                "type": "fila.atualizada",
                "queue": nomes
            }
        )

    @sync_to_async
    def get_usuario_id_da_sessao(self):
        return self.scope["session"].get("usuario_id")

    @sync_to_async
    def get_nome_usuario(self, usuario_id):
        return self.scope["session"].get("usuario_nome", f"Desconhecido ({usuario_id})")
