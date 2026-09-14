from fastapi import APIRouter, Depends
from models import User #para buscar a tabela de usuário do banco de dado
from dependencies import pegar_sessao


auth_router = APIRouter(prefix="/auth", tags=["auth"]) 
#prefix: importante ter um prefixo: para não ter conflitâncias e orgranização
#tags: Vai para a documentação da APi no fastAPI

@auth_router.get("/")
async def home():
    '''
    Essa é a rota padrão de autenticação de meu sistema
   '''
    return{
        "Mensagem": "Você acessou a rota padrão de autenticação ",
        "Autenticado": False,}

#-----------------------------------------------------------------------------------------------------------------

@auth_router.post("/criar_conta")# Criar
#Criando a função assíncrona -> async
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    usuario = session.query(User).filter(User.email==email).first() #Realiza uma query/consulta no banco de dados
    #Verificando se o usuário existe
    if usuario:
        #já existe um usuário com esse email
        return {"Mensagem": "Já existe um usuário com esse email!"}

    else:
        #cria um novo usuário
        novo_user = User(nome, email, senha)
        session.add(novo_user)
        session.commit()
        return {"Mensagem": "Usuário cadastrado com sucesso!"}


    
    