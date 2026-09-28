#Classes pydantic para validação de dados de entrada e saída da API -> forca a tipagem de dados e validação de dados
# integriade dos dados
#padronizar os parametro de usuário

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):#Herdando o BaseModel
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config: # para ser interpretado como um objeto -> para conectar a classe com o modelo
        from_attributes = True