from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["orders"])

@order_router.get("/")
async def pedidos():
    '''
    Essa é a rota padrão de pedidos do meu sistema. Todas as rotas dos pedidos precisam de autenticação
    '''
    #DocString explica a API

    return{"mensagem": "Você acessou a rota de pedidos"} #Retorna a mensagem, resultado e etc em JSON para o RestAPI e aparecer no site
