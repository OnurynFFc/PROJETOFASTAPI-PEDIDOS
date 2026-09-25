#executando no servidor a Api pelo terminal
#main = nome do arquivo. "main" é um padrão de boa prática
# uvicorn main:app --reload

#Importando o FastAPI
from fastapi import FastAPI
# from passlib.context import CryptContext
import bcrypt
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") # chaves de segurança para o JWT

app = FastAPI()

# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #definindo o esquema de criptografia para senhas
#decrepated="auto" -> para não usar mais o esquema antigo de criptografia

from order_routes import order_router
from auth_routes import auth_router 

#endpoints:
#/orders
app.include_router(auth_router)
#/auth
app.include_router(order_router)




#Rest APIs
#GET -> Leitura/pegar
#POST -> Enviar/Criar
#PUT/PACTH -> Edição
#DELETE -> Deletar

