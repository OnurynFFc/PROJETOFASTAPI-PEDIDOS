from models import User, db #para buscar a tabela de usuário do banco de dado
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)#abrindo a sessão com conexão no banco de dados
        session = Session()#sessão aberta no banco

        yield session 
        # pega o primeiro elemento da lista, neste caso -> não encerra a função, retorna o valor sem encerrar a execução da função
        #funciona quando estiver termindado de usar a sessão
    finally: 
        #se der algum erro, fecha a sessão
        session.close()
        