class NoLista:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def inserir_fim(self, valor):
        novo = NoLista(valor)
        if self.inicio is None:
            self.inicio = novo
            self.fim = novo
        else:
            self.fim.proximo = novo
            self.fim = novo
        self.tamanho += 1

    def inserir_inicio(self, valor):
        novo = NoLista(valor)
        novo.proximo = self.inicio
        self.inicio = novo
        if self.fim is None:
            self.fim = novo
        self.tamanho += 1

    def remover_por_id(self, id_ocorrencia):
        anterior = None
        atual = self.inicio

        while atual is not None:
            if atual.valor.id == id_ocorrencia:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                if atual == self.fim:
                    self.fim = anterior

                self.tamanho -= 1
                return atual.valor

            anterior = atual
            atual = atual.proximo

        return None

    def contem_id(self, id_ocorrencia):
        atual = self.inicio
        while atual is not None:
            if atual.valor.id == id_ocorrencia:
                return True
            atual = atual.proximo
        return False

    def copiar(self):
        copia = ListaEncadeada()
        atual = self.inicio
        while atual is not None:
            copia.inserir_fim(atual.valor)
            atual = atual.proximo
        return copia

    def esta_vazia(self):
        return self.inicio is None

    def __bool__(self):
        return not self.esta_vazia()

    def __iter__(self):
        atual = self.inicio
        while atual is not None:
            yield atual.valor
            atual = atual.proximo


class RegistroHistorico:
    def __init__(self, descricao, tipo, ocorrencia=None, numero=0, numero_desfeito=None):
        self.descricao = descricao
        self.tipo = tipo
        self.ocorrencia = ocorrencia
        self.numero = numero
        self.numero_desfeito = numero_desfeito


class NoPilha:
    def __init__(self, registro):
        self.registro = registro
        self.proximo = None


class PilhaHistorico:
    def __init__(self):
        self.topo = None
        self.proximo_numero = 1

    def registrar(self, descricao, tipo, ocorrencia=None):
        novo = NoPilha(RegistroHistorico(descricao, tipo, ocorrencia, self.proximo_numero))
        novo.proximo = self.topo
        self.topo = novo
        self.proximo_numero += 1

    def listar(self):
        descricoes = ListaEncadeada()
        atual = self.topo
        while atual is not None:
            descricoes.inserir_fim(atual.registro.descricao)
            atual = atual.proximo
        return descricoes

    def buscar_ultima_acao_desfazivel(self):
        atual = self.topo
        while atual is not None:
            registro = atual.registro
            if self._pode_desfazer(registro):
                return registro
            atual = atual.proximo
        return None

    def registrar_desfazer(self, registro_desfeito, descricao):
        novo = NoPilha(
            RegistroHistorico(
                descricao,
                "desfazer",
                registro_desfeito.ocorrencia,
                self.proximo_numero,
                registro_desfeito.numero,
            )
        )
        novo.proximo = self.topo
        self.topo = novo
        self.proximo_numero += 1

    def _pode_desfazer(self, registro):
        if registro.tipo != "cadastro" and registro.tipo != "atendimento":
            return False
        return not self._foi_desfeito(registro.numero)

    def _foi_desfeito(self, numero_registro):
        atual = self.topo
        while atual is not None:
            registro = atual.registro
            if registro.tipo == "desfazer" and registro.numero_desfeito == numero_registro:
                return True
            atual = atual.proximo
        return False


class NoFila:
    def __init__(self, ocorrencia):
        self.ocorrencia = ocorrencia
        self.proximo = None


class FilaAtendimento:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, ocorrencia):
        novo = NoFila(ocorrencia)
        if self.inicio is None:
            self.inicio = novo
            self.fim = novo
        else:
            self.fim.proximo = novo
            self.fim = novo

    def desenfileirar_aberta(self):
        while self.inicio is not None:
            atual = self.inicio
            self.inicio = atual.proximo
            if self.inicio is None:
                self.fim = None
            if atual.ocorrencia.status == "Aberto":
                return atual.ocorrencia
        return None


class NoArvore:
    def __init__(self, chave, ocorrencia):
        self.chave = chave
        self.ocorrencia = ocorrencia
        self.esquerda = None
        self.direita = None


class ArvoreBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, ocorrencia):
        if self.raiz is None:
            self.raiz = NoArvore(chave, ocorrencia)
            return
        self._inserir(self.raiz, chave, ocorrencia)

    def _inserir(self, no, chave, ocorrencia):
        if chave == no.chave:
            raise ValueError("Já existe uma ocorrência com esse ID.")
        if chave < no.chave:
            if no.esquerda is None:
                no.esquerda = NoArvore(chave, ocorrencia)
            else:
                self._inserir(no.esquerda, chave, ocorrencia)
        else:
            if no.direita is None:
                no.direita = NoArvore(chave, ocorrencia)
            else:
                self._inserir(no.direita, chave, ocorrencia)

    def buscar(self, chave):
        atual = self.raiz
        while atual is not None:
            if chave == atual.chave:
                return atual.ocorrencia
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None


class NoHeap:
    def __init__(self, ocorrencia, pai=None):
        self.ocorrencia = ocorrencia
        self.pai = pai
        self.esquerda = None
        self.direita = None


class MaxHeapPrioridade:
    def __init__(self):
        self.raiz = None
        self.tamanho = 0

    def inserir(self, ocorrencia):
        self.tamanho += 1
        novo = NoHeap(ocorrencia)

        if self.raiz is None:
            self.raiz = novo
            return

        pai = self._buscar_no(self.tamanho // 2)
        novo.pai = pai
        if self.tamanho % 2 == 0:
            pai.esquerda = novo
        else:
            pai.direita = novo

        self._subir(novo)

    def extrair_aberta(self):
        while self.raiz is not None:
            maior = self._extrair_maior()
            if maior.status == "Aberto":
                return maior
        return None

    def _extrair_maior(self):
        maior = self.raiz.ocorrencia

        if self.tamanho == 1:
            self.raiz = None
            self.tamanho = 0
            return maior

        ultimo = self._buscar_no(self.tamanho)
        self.raiz.ocorrencia = ultimo.ocorrencia

        if ultimo.pai.esquerda == ultimo:
            ultimo.pai.esquerda = None
        else:
            ultimo.pai.direita = None

        self.tamanho -= 1
        self._descer(self.raiz)
        return maior

    def _buscar_no(self, posicao):
        atual = self.raiz
        divisor = 1

        while divisor * 2 <= posicao:
            divisor *= 2

        divisor //= 2
        while divisor >= 1:
            if posicao // divisor % 2 == 0:
                atual = atual.esquerda
            else:
                atual = atual.direita
            divisor //= 2

        return atual

    def _tem_maior_prioridade(self, a, b):
        if a.prioridade != b.prioridade:
            return a.prioridade > b.prioridade
        return a.ordem_chegada < b.ordem_chegada

    def _trocar_ocorrencias(self, a, b):
        temporario = a.ocorrencia
        a.ocorrencia = b.ocorrencia
        b.ocorrencia = temporario

    def _subir(self, no):
        atual = no
        while atual.pai is not None:
            if not self._tem_maior_prioridade(atual.ocorrencia, atual.pai.ocorrencia):
                break
            self._trocar_ocorrencias(atual, atual.pai)
            atual = atual.pai

    def _descer(self, no):
        atual = no
        while atual is not None:
            maior = atual

            if (
                atual.esquerda is not None
                and self._tem_maior_prioridade(atual.esquerda.ocorrencia, maior.ocorrencia)
            ):
                maior = atual.esquerda

            if (
                atual.direita is not None
                and self._tem_maior_prioridade(atual.direita.ocorrencia, maior.ocorrencia)
            ):
                maior = atual.direita

            if maior == atual:
                break

            self._trocar_ocorrencias(atual, maior)
            atual = maior


class EntradaHash:
    def __init__(self, chave, ocorrencia):
        self.chave = chave
        self.ocorrencia = ocorrencia
        self.proximo = None


class BaldeHash:
    def __init__(self, indice):
        self.indice = indice
        self.entrada = None
        self.proximo = None

    def inserir(self, chave, ocorrencia):
        nova = EntradaHash(chave, ocorrencia)
        nova.proximo = self.entrada
        self.entrada = nova


class HashOcorrencias:
    def __init__(self, tamanho=31):
        self.tamanho = tamanho
        self.baldes = self._criar_baldes(tamanho)

    def inserir(self, chave, ocorrencia):
        chave_normalizada = self._normalizar(chave)
        indice = self._hash(chave_normalizada)
        self._obter_balde(indice).inserir(chave_normalizada, ocorrencia)

    def buscar(self, chave):
        chave_normalizada = self._normalizar(chave)
        indice = self._hash(chave_normalizada)
        entrada = self._obter_balde(indice).entrada
        resultados = ListaEncadeada()

        while entrada is not None:
            if (
                entrada.chave == chave_normalizada
                and not resultados.contem_id(entrada.ocorrencia.id)
            ):
                resultados.inserir_fim(entrada.ocorrencia)
            entrada = entrada.proximo

        return resultados

    def _criar_baldes(self, tamanho):
        primeiro = BaldeHash(0)
        atual = primeiro
        indice = 1

        while indice < tamanho:
            atual.proximo = BaldeHash(indice)
            atual = atual.proximo
            indice += 1

        return primeiro

    def _obter_balde(self, indice):
        atual = self.baldes
        while atual.indice != indice:
            atual = atual.proximo
        return atual

    def _hash(self, chave):
        total = 0
        for caractere in chave:
            total = (total * 31 + ord(caractere)) % self.tamanho
        return total

    def _normalizar(self, chave):
        return chave.strip().lower()
