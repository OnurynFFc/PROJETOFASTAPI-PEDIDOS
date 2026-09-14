#executando no servidor a Api pelo terminal
#main = nome do arquivo. "main" é um padrão de boa prática
# uvicorn main:app --reload

#Importando o FastAPI
from fastapi import FastAPI

app = FastAPI()

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

