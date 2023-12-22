# Imagem do pitão
FROM python:3

# Comandos futuros serão feitos aqui dentro
WORKDIR /servidor_docker

# "pasta_origem" vai para "pasta_destino"
COPY . /servidor_docker

# Instalar todas as dependências desse texto (isso pegará o requirements.txt copiado da pasta_origem
# já que estamos usando como workdir o servidor_docker)
#RUN ping -c 4 142.251.128.78
#RUN curl -sSf http://142.251.128.78 || exit 1
#RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && pip install pipenv && pipenv install --system
RUN apt-get update
RUN apt-get install -y supervisor
RUN pip3 install -r requirements.txt

#"pip3", "install", "-r", "requirements.txt"

# Convenção de porta do host
EXPOSE 8000

# ENV poderia colocar variaveis do sistema aqui

# Comando para rodar o servidor django e o celery quando o contâiner foir ativado. Adicionar coisas dentro dessa string

# execução do supervisord
#CMD ["ping", "-c", "4", "142.251.128.78"]
#CMD ["curl", "-ssf", "http://142.251.128.78", "||", "exit", "1"]
CMD ["supervisord", "-c", "projeto_configuracoes/supervisord.conf"]


