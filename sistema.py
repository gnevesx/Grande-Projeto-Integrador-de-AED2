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
        if copia.esta_vazia() or copia.inicio.proximo is None:
            return copia

        copia.inicio = self._ordenar_por_mesclagem(copia.inicio, campo)

        atual = copia.inicio
        while atual is not None and atual.proximo is not None:
            atual = atual.proximo
        copia.fim = atual

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
            if ocorrencia.ordem_chegada == self._proxima_ordem - 1:
                self._proxima_ordem -= 1
            self._reconstruir_estruturas()
            mensagem = f"Cadastro desfeito. Ocorrência ID {ocorrencia.id} removida."
            self.historico.registrar_desfazer(registro, mensagem)
            return mensagem

        return None

    def _ordenar_por_mesclagem(self, no_inicial, campo):
        if no_inicial is None or no_inicial.proximo is None:
            return no_inicial

        meio = self._obter_meio(no_inicial)
        proxima_metade = meio.proximo
        meio.proximo = None

        esquerda = self._ordenar_por_mesclagem(no_inicial, campo)
        direita = self._ordenar_por_mesclagem(proxima_metade, campo)

        return self._mesclar_ordenado(esquerda, direita, campo)

    def _obter_meio(self, no_inicial):
        if no_inicial is None:
            return no_inicial

        lento = no_inicial
        rapido = no_inicial.proximo

        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo

        return lento

    def _mesclar_ordenado(self, a, b, campo):
        if a is None:
            return b
        if b is None:
            return a

        if not self._maior_que(a.valor, b.valor, campo):
            a.proximo = self._mesclar_ordenado(a.proximo, b, campo)
            return a
        b.proximo = self._mesclar_ordenado(a, b.proximo, campo)
        return b

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
