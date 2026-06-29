import json
import os
from modelos import Ocorrencia
from estruturas import PilhaHistorico, RegistroHistorico, NoPilha
from sistema import SistemaOcorrencias

ARQUIVO_ESTADO = "estado_sistema.json"

def _ocorrencia_para_dict(ocorrencia):
    return {
        "id": ocorrencia.id,
        "nome": ocorrencia.nome,
        "tipo": ocorrencia.tipo,
        "descricao": ocorrencia.descricao,
        "prioridade": ocorrencia.prioridade,
        "ordem_chegada": ocorrencia.ordem_chegada,
        "status": ocorrencia.status,
    }

def _dict_para_ocorrencia(ocorrencia_dict):
    return Ocorrencia(**ocorrencia_dict)

def _registro_para_dict(registro):
    return {
        "descricao": registro.descricao,
        "tipo": registro.tipo,
        "ocorrencia_id": registro.ocorrencia.id if registro.ocorrencia else None,
        "numero": registro.numero,
        "numero_desfeito": registro.numero_desfeito,
    }

def _dict_para_registro(registro_dict, ocorrencias_por_id):
    ocorrencia = None
    if registro_dict["ocorrencia_id"] is not None:
        ocorrencia = ocorrencias_por_id.get(registro_dict["ocorrencia_id"])
    return RegistroHistorico(
        descricao=registro_dict["descricao"],
        tipo=registro_dict["tipo"],
        ocorrencia=ocorrencia,
        numero=registro_dict["numero"],
        numero_desfeito=registro_dict["numero_desfeito"],
    )

def salvar_estado(sistema: SistemaOcorrencias):
    dados = {
        "proximo_id": sistema._proximo_id,
        "proxima_ordem": sistema._proxima_ordem,
        "ocorrencias": [],
        "historico": [],
    }

    for ocorrencia in sistema.lista_geral:
        dados["ocorrencias"].append(_ocorrencia_para_dict(ocorrencia))

    temp_historico_list = []
    atual = sistema.historico.topo
    while atual:
        temp_historico_list.append(_registro_para_dict(atual.registro))
        atual = atual.proximo
    dados["historico"] = temp_historico_list[::-1]

    try:
        with open(ARQUIVO_ESTADO, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Estado do sistema salvo em '{ARQUIVO_ESTADO}'.")
    except IOError as e:
        print(f"Erro ao salvar o estado do sistema: {e}")

def carregar_estado():
    if not os.path.exists(ARQUIVO_ESTADO):
        print(f"Arquivo de estado '{ARQUIVO_ESTADO}' não encontrado. Iniciando novo sistema.")
        return SistemaOcorrencias()

    try:
        with open(ARQUIVO_ESTADO, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao carregar o estado do sistema (JSON inválido): {e}. Iniciando novo sistema.")
        return SistemaOcorrencias()
    except IOError as e:
        print(f"Erro ao carregar o estado do sistema: {e}. Iniciando novo sistema.")
        return SistemaOcorrencias()

    sistema = SistemaOcorrencias()

    sistema._proximo_id = dados.get("proximo_id", 1)
    sistema._proxima_ordem = dados.get("proxima_ordem", 1)

    ocorrencias_por_id = {}
    for ocorrencia_dict in dados.get("ocorrencias", []):
        ocorrencia = _dict_para_ocorrencia(ocorrencia_dict)
        sistema.lista_geral.inserir_fim(ocorrencia)
        ocorrencias_por_id[ocorrencia.id] = ocorrencia

    sistema.historico = PilhaHistorico()
    for registro_dict in dados.get("historico", []):
        registro = _dict_para_registro(registro_dict, ocorrencias_por_id)
        novo_no_pilha = NoPilha(registro)
        novo_no_pilha.proximo = sistema.historico.topo
        sistema.historico.topo = novo_no_pilha
        if registro.numero >= sistema.historico.proximo_numero:
            sistema.historico.proximo_numero = registro.numero + 1

    sistema._reconstruir_estruturas()

    print(f"Estado do sistema carregado de '{ARQUIVO_ESTADO}'.")
    return sistema