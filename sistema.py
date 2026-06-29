from estruturas import (
    ArvoreBusca,
    FilaAtendimento,
    HashOcorrencias,
    ListaEncadeada,
    MaxHeapPrioridade,
    PilhaHistorico,
)
from modelos import Ocorrencia


class SistemaOcorrencias:
    def __init__(self):
        self.lista_geral = ListaEncadeada()
        self.fila = FilaAtendimento()
        self.arvore = ArvoreBusca()
        self.heap = MaxHeapPrioridade()
        self.tabela_hash = HashOcorrencias()
        self.historico = PilhaHistorico()
        self._proximo_id = 1
        self._proxima_ordem = 1

    def cadastrar(self, nome, tipo, descricao, prioridade):
        self._validar_prioridade(prioridade)
        id_ocorrencia = self._gerar_id()

        ocorrencia = Ocorrencia(
            id=id_ocorrencia,
            nome=nome,
            tipo=tipo,
            descricao=descricao,
            prioridade=prioridade,
            ordem_chegada=self._proxima_ordem,
            status="Aberto",
        )
        self._proxima_ordem += 1

        self.lista_geral.inserir_fim(ocorrencia)
        self.fila.enfileirar(ocorrencia)
        self.arvore.inserir(ocorrencia.id, ocorrencia)
        self.heap.inserir(ocorrencia)
        self.tabela_hash.inserir(ocorrencia.nome, ocorrencia)
        self.tabela_hash.inserir(ocorrencia.tipo, ocorrencia)
        self.historico.registrar(f"Cadastro da ocorrência ID {ocorrencia.id}", "cadastro", ocorrencia)
        return ocorrencia

    def listar_todas(self):
        return self.lista_geral

    def atender_por_chegada(self):
        ocorrencia = self.fila.desenfileirar_aberta()
        if ocorrencia is None:
            return None
        ocorrencia.status = "Atendido"
        self.historico.registrar(f"Atendimento por fila da ocorrência ID {ocorrencia.id}", "atendimento", ocorrencia)
        return ocorrencia

    def atender_por_prioridade(self):
        ocorrencia = self.heap.extrair_aberta()
        if ocorrencia is None:
            return None
        ocorrencia.status = "Atendido"
        self.historico.registrar(f"Atendimento por prioridade da ocorrência ID {ocorrencia.id}", "atendimento", ocorrencia)
        return ocorrencia

    def buscar_por_id(self, id_ocorrencia):
        return self.arvore.buscar(id_ocorrencia)

    def buscar_por_nome_ou_tipo(self, chave):
        return self.tabela_hash.buscar(chave)

    def ordenar_ocorrencias(self, campo):
        self._validar_campo_ordenacao(campo)
        copia = self.lista_geral.copiar()
        if copia.esta_vazia():
            return copia

        houve_troca = True

        while houve_troca:
            houve_troca = False
            atual = copia.inicio
            while atual is not None and atual.proximo is not None:
                if self._maior_que(atual.valor, atual.proximo.valor, campo):
                    temporario = atual.valor
                    atual.valor = atual.proximo.valor
                    atual.proximo.valor = temporario
                    houve_troca = True
                atual = atual.proximo

        return copia

    def ver_historico(self):
        return self.historico.listar()

    def desfazer_ultima_acao(self):
        registro = self.historico.buscar_ultima_acao_desfazivel()
        if registro is None:
            return None

        tipo = registro.tipo
        ocorrencia = registro.ocorrencia

        if tipo == "atendimento":
            ocorrencia.status = "Aberto"
            self._reconstruir_estruturas()
            mensagem = f"Atendimento desfeito. Ocorrência ID {ocorrencia.id} voltou para Aberto."
            self.historico.registrar_desfazer(registro, mensagem)
            return mensagem

        if tipo == "cadastro":
            self.lista_geral.remover_por_id(ocorrencia.id)
            if ocorrencia.id == self._proximo_id - 1:
                self._proximo_id -= 1
            if ocorrencia.ordem_chegada == self._proxima_ordem - 1:
                self._proxima_ordem -= 1
            self._reconstruir_estruturas()
            mensagem = f"Cadastro desfeito. Ocorrência ID {ocorrencia.id} removida."
            self.historico.registrar_desfazer(registro, mensagem)
            return mensagem

        return None

    def _maior_que(self, a, b, campo):
        if campo == "id":
            return a.id > b.id
        if campo == "prioridade":
            return a.prioridade < b.prioridade
        if campo == "nome":
            return a.nome.lower() > b.nome.lower()

    def _validar_campo_ordenacao(self, campo):
        if campo != "id" and campo != "prioridade" and campo != "nome":
            raise ValueError("Campo de ordenação inválido.")

    def _validar_prioridade(self, prioridade):
        if prioridade < 1 or prioridade > 5:
            raise ValueError("Prioridade deve estar entre 1 e 5.")

    def _gerar_id(self):
        id_ocorrencia = self._proximo_id
        self._proximo_id += 1
        return id_ocorrencia

    def _reconstruir_estruturas(self):
        self.fila = FilaAtendimento()
        self.arvore = ArvoreBusca()
        self.heap = MaxHeapPrioridade()
        self.tabela_hash = HashOcorrencias()

        for ocorrencia in self.lista_geral:
            self.arvore.inserir(ocorrencia.id, ocorrencia)
            self.tabela_hash.inserir(ocorrencia.nome, ocorrencia)
            self.tabela_hash.inserir(ocorrencia.tipo, ocorrencia)
            if ocorrencia.status == "Aberto":
                self.fila.enfileirar(ocorrencia)
                self.heap.inserir(ocorrencia)
