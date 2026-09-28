from fastapi import APIRouter, Depends, HTTPException
from models import User #para buscar a tabela de usuário do banco de dado
from dependencies import pegar_sessao
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
# from main import bcrypt_context

import bcrypt

auth_router = APIRouter(prefix="/auth", tags=["auth"]) 
#prefix: importante ter um prefixo: para não ter conflitâncias e orgranização
#tags: Vai para a documentação da APi no fastAPI


#função para criptografar a senha do usuário
def hash_password(password: str) -> str:
    #converte a senha para bytes
    password_bytes = password.encode('utf-8')
    #gera um salt aleatório
    salt = bcrypt.gensalt()
    hashed_senha = bcrypt.hashpw(password_bytes, salt)
    return hashed_senha.decode('utf-8')  # Retorna a senha criptografada como string

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
async def criar_conta(usuario_schema:UsuarioSchema, session: Session= Depends(pegar_sessao)):
    #entrada
    usuario = session.query(User).filter(User.email==usuario_schema.email).first() #Realiza uma query/consulta no banco de dados
    #Verificando se o usuário existe
    if usuario:
        #já existe um usuário com esse email
        #saída
        raise HTTPException(status_code=400, detail="Usuário cadastrado") #levantando uma exceção HTTP com status code 400 e detalhe "Usuário cadastrado"
    else:
        #criptografando a senha do usuário
        senha_criptografada = hash_password(usuario_schema.senha)
        #cria um novo usuário
        novo_user = User(usuario_schema.nome, usuario_schema.email, senha_criptografada)
        session.add(novo_user)
        session.commit()
        return {"Mensagem": f"Usuário cadastrado com sucesso! {usuario_schema.email}"}


    
    