from dataclasses import dataclass


@dataclass
class Ocorrencia:
    id: int
    nome: str
    tipo: str
    descricao: str
    prioridade: int
    ordem_chegada: int
    status: str
