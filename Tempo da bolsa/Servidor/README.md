

# Documentação da dashboard-nginx


O objetivo desse conjunto de código é o de exibir uma dashboard com os valores da dashboard bibubga: bobinho.com. Com intuito de manter os dados de maneira mais constante em um banco de dados nosso e com a possibilidade de melhora e manutenção de uma dashboard feita com código próprio. Assim servindo como uma dashboard sucessora.

Códigos iniciais produzidos: Foram criados vários scripts iniciais que estão dentro da pasta “Códigos Python”, e na subpasta de “SQL scripts dentro do python” que contém scripts iniciais da conexão com mysql connector do python com o banco de dados. Esses scripts podem ser rodados individualmente sem problemas, eles modificam a base de dados (no caso iniciam ela com os dados da dashboard antiga), ou manipulam os dados para algum propósito:

* CriaJsonExemplo: cria um exemplo de arquivo JSON extraido da dashboard nginx. (útil para entender a estrutura do JSON separadamente do código). O nome do arquivo é “conteudo”. A fonte do JSON é diretamente da dashboard.

* DecodificadorJson: Soma os valores de todos os JSONS adquiridos através do banco de dados e printa o resultado.

* ParserReal: Adquire todos os JSONS de todos os dias da dashboard e os coloca dentro de um arquivo chamado “conteudo”

* ParserSQL: Funcionalmente igual o ParserReal, a diferença é que não escreve no arquivo, mas insere no banco de dados SQL dentro da table “Json”. Todos os dias da dashboard até o dia de hoje serão inseridos. (repete inserções, não pode usar quantas vezes quiser)

* ParserSQLcomdata: Funcionalmente similar o ParserSQL. A diferença é que esse é um parser que insere valores no banco de dados  mais atual no sentido de que uma segunda informação é adicionada no Json chamada “data”. Usando data, se verifica se aquele Json já existe na table, impedindo a repetição dentro do banco de dados dos valores Json. Ele também calcula o tempo que demorou para cada processo relevante, útil para o debug relacionado à otimização 

* Testes e Testes2: Um arquivo de testes da linguagem python. Nada de especial.

* TrocadordeHTML: Pega todos os jsons do banco de dados, soma todos os valores dos jsons em um único json e depois substitui o valor json bruto do html pelos novos valores somados. Isso então substitui um HTML com json de um dia, pelo json somado de todos os dias. Útil para conseguir usar um template do HTML com os novos valores somados

* Os testes fazem o que o nome de cada um diz. o delete deleta todos os valores da table json, o insert insere um valor exemplo, o select faz select de um valor exemplo, o update dá update em um valor exemplo.

Existe também a pasta “Códigos Node,Js”. Foram os primeiros códigos de tentar criar um parser para extrair os jsons do html bruto da dashboard-nginx. O código não está completo. Também tem um script de testes para as funcionalidades do javascript. Era para ter sido feito em Node.Js (como o próprio nome diz).

A pasta ScriptsSQL contém todos os scripts de SQL que eu utilizei para a criação de todas as tables e manipulações específicas delas dentro do SQL. Comentarei das mais importantes:

* Todos os dashboard_alguma_coisa. Alguns não estão completos, outros não funcionam corretamente. Mas os que eu sei da funcionalidade e que estão corretos são o dashboard_requests, dashboard_general.

* Script de remover valores de todas as tables (Truncante precisa ser usado ao invés de delete nesse caso por que as duas dashboards tem chaves estrangeiras ligadas à table json, impedindo que sejam removidas sem remover também essas chaves)

* Os outros Scripts contém códigos interessantes mas não necessariamente relevantes para a continuidade da construção da dashboard-nginx.

* O ambiente virtual correto é o ambiente virtual que fica dentro da pasta Servidor caso queira rodar o código corretamente, pois dentro dessa pasta é onde se encontra o código django, com as configurações Docker, correto sendo o uso do docker-compose.yml (ele junta todos os contêineres, só tem um por enquanto), do supervisord (iniciador dos processos), do celery worker (fazedor de coisas que estão na fila do schedule) e do celery beat (o scheduler) usando RabbitMQ. Se quiser reiniciar o ambiente virtual só utilizar o requirements.txt, "pip install -r requirements.txt" enquanto estiver na pasta Servidor".

Para iniciar o servidor, é só chamar o “docker-compose up -d”, assim rodará o servidor em segundo plano graças ao -d. Algumas views já foram mapeadas:

* Para verificar o status do docker-compose que está sendo rodado em plano de fundo, utilizar o comando "sudo docker-compose logs -f". Isso mostrará o log em tempo real dele (e de outros caso tenham). Pode usar também "sudo docker-compose ps", para mostrar todos os containeres que tem estado up atualmente

* A view dashboard_general sendo a mais importante de todas as views.

* As outras são testes com templates ou hello worlds.

* O template mais importante que trabalha em conjunto com a view dashboard_general é o template “dashboard_general.html”

Pontos importantes para o servidor funcionar:

* Ao iniciar o servidor diretamente com python3 manage.py runserver, precisa inserir algum input qualquer para o servidor entrar no ar, se não ele fica preso em um estado de “system check”

* As URLS já foram mepeadas corretamente, não tem necessidade de modificá-las a não ser se o nome do app django (a pasta onde meu código django que não são configurações está) mudar para algo além de “teste”.

* Ao iniciar o docker-compose, o dockerfile será usado para criar uma imagem do servidor e expor a porta 8000:8000. Depois que o dockerfile criar o contêiner, o supervisord será chamado para ativar o servidor Django, o celery_worker e o celery_beat (nosso scheduler). Com esses 3 aplicativos diferentes abertos, de 1 em 1 dia o script “script inicial” será chamado. ele atualizará os valores das tables automaticamente enquanto a imagem docker estiver de pé todo dia, usando o celery.

* Para resetar a imagem do docker-compose ao iniciar é só usar o comando ““sudo docker-compose up --build -d” para que a imagem seja feita novamente, como também seja rodado em segundo plano.




