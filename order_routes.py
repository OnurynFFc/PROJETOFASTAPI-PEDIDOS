from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/order", tags=["orders"])

@order_router.get("/")
async def pedidos():
    '''
    Essa é a rota padrão de pedidos do meu sistema. Todas as rotas dos pedidos precisam de autenticação
    '''
    #DocString explica a API

    return{"mensagem": "Você acessou a rota de pedidos"} #Retorna a mensagem, resultado e etc em JSON para o RestAPI e aparecer no site


@order_router.post("/pedido")
#criando em pedido
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)# puxando pelo id do uuário
    session.add(novo_pedido)
    session.commit()
    return{"Mensagem": f"Pedido feito com sucesso. ID do pedido: {novo_pedido.id}"}