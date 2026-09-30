from fastapi import APIRouter, Depends, HTTPException
from models import User #para buscar a tabela de usuário do banco de dado
from dependencies import pegar_sessao
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from datetime import datetime,timedelta, timezone

from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY

import bcrypt

auth_router = APIRouter(prefix="/auth", tags=["auth"]) 
#prefix: importante ter um prefixo: para não ter conflitâncias e ter orgranização
#tags: Vai para a documentação da APi no fastAPI

#função para criptografar a senha do usuário
def hash_password(password: str) -> str:
    #converte a senha para bytes
    password_bytes = password.encode('utf-8')
    #gera um salt -> aleatório
    salt = bcrypt.gensalt()
    hashed_senha = bcrypt.hashpw(password_bytes, salt)
    return hashed_senha.decode('utf-8')  # Retorna a senha criptografada como string

#criar Token 
def criar_token(id_usuario):
    # JWT
    #determnando uma tempo de expiração do token = fuso 0 + deltatime do acees token (definido no main)
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_infomarcoes ={
        "sub":id_usuario, #id do usuário
        "exp": data_expiracao
    }
    jwt_cod =jwt.encode(dic_infomarcoes,SECRET_KEY,ALGORITHM)#Token codificado
    # token = jwt_cod
    return jwt_cod

#Autenticação de ususario -> login e senha (descriptografar a senha hash)
def autenticar_usuario(email,senha,session):
    #faz uma consulta no banco -> filtrando se o email é o mesmo cadastrado no banco de dados
    usuario = session.query(User).filter(User.email==email).first()
    
    if not usuario:
        return False #não existir o email
    elif bcrypt_context.verify(senha, usuario.senha):#verifica senha
        return False #não for a mesma senha
    #Acesso negado
    return usuario #Acesso liberado
   

@auth_router.get("/")
async def home():

    '''
    Essa é a rota padrão de autenticação de meu sistema
   '''
    return{
        "Mensagem": "Você acessou a rota padrão de autenticação ",
        "Autenticado": False,
        }

#-----------------------------------------------------------------------------------------------------------------

@auth_router.post("/criar_conta")# Criar
#Criando a função assíncrona -> async
async def criar_conta(usuario_schema:UsuarioSchema, session: Session=Depends(pegar_sessao)):
    #entrada
    usuario = session.query(User).filter(User.email==usuario_schema.email).first() #Realiza uma query/consulta no banco de dados
    #Verificando se o usuário existe
    if usuario:
        #já existe um usuário com esse email
        #saída
        raise HTTPException(status_code=400, detail="Usuário já cadastrado") #levantando uma exceção HTTP com status code 400 e detalhe "Usuário cadastrado"
    else:
        #criptografando a senha do usuário
        senha_criptografada = hash_password(usuario_schema.senha)
        #cria um novo usuário
        novo_user = User(usuario_schema.nome, usuario_schema.email, senha_criptografada)
        session.add(novo_user)
        session.commit()
        return {"Mensagem": f"Usuário cadastrado com sucesso! {usuario_schema.email}"}


    
#login -> email e senha -> Token JWT (json web token)    

@auth_router.post("/login")
async def login(login_schema: LoginSchema ,session: Session= Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)#Verifica se o usuario existe -> email, senha, seassão
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        #gerar token para usuário
        access_token = criar_token(usuario.id)
        return {
            "access token": access_token,
            "token_type": "Bearer"
            }
    
        #JWT Bearer
        #headers ={"Access-Token":"Bearer token"}

