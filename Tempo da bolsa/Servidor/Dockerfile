# Imagem do pitão
FROM python:3

# Comandos futuros serão feitos aqui dentro
WORKDIR /servidor_docker

# "pasta_origem" vai para "pasta_destino"
COPY . /servidor_docker

# Instalar todas as dependências desse texto (isso pegará o requirements.txt copiado da pasta_origem
# já que estamos usando como workdir o servidor_docker)
RUN apt-get update
RUN apt-get install -y supervisor
RUN pip3 install -r requirements.txt

#"pip3", "install", "-r", "requirements.txt"

# Convenção de porta do host
EXPOSE 8000

# ENV poderia colocar variaveis do sistema aqui

# Comando para rodar o servidor django e o celery quando o contâiner foir ativado. Adicionar coisas dentro dessa string

# execução do supervisord
CMD ["supervisord", "-c", "projeto_configuracoes/supervisord.conf"]


