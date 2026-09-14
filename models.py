from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


#Conexão com o banco
db = create_engine("sqlite:///banco.db")#como parâmetro colocar o link do banco de dados. Adaptar quando for fazer o deploy do projeto

#Base do banco de dados
base = declarative_base()

#Criar as classes do banco -> tabelas (depende do modelo de negócio -> qual é a finalidade da aplicação)
#user
class User(base):
    __tablename__ ="usuarios" #Nome da tabela

    #Column (nome da coluna, tipo, nulo ou não) nullable: se é nulo ou não -> regra de negócio
    #default = paramentros padrão
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email",String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    #quando criar um usuário com py, o que vai acontecer. Sempre quando na tabela
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#Pedido
class Pedido(base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS=(
    #     ("PENDENTE", "PENDETE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)# Pendente, cancelado e finalizado -> ChoiceType(choices=STATUS_PEDIDOS)
    usuario = Column("usuario",ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens =

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

#ItensPedido
class ItensPedido(base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, default=1)
    sabor = Column("sabor", String)
    tamanho= Column("tamanho", String)
    preco_unitario= Column("preco_unitario", Float)
    pedido= Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario,pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido =pedido

#

#Executa a criação dos metadados do seu banco de dados(cria de fato o Banco de Dados)
