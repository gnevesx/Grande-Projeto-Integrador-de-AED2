class PilhaHistorico:
    def __init__(self):
        self._dados = []

    def registrar(self, descricao, tipo, ocorrencia=None):
        self._dados.append({
            "descricao": descricao,
            "tipo": tipo,
            "ocorrencia": ocorrencia,
        })

    def listar(self):
        return [registro["descricao"] for registro in reversed(self._dados)]

    def desfazer(self):
        if not self._dados:
            return None
        return self._dados.pop()


class FilaAtendimento:
    def __init__(self):
        self._dados = []
        self._inicio = 0

    def enfileirar(self, ocorrencia):
        self._dados.append(ocorrencia)

    def desenfileirar_aberta(self):
        while self._inicio < len(self._dados):
            ocorrencia = self._dados[self._inicio]
            self._inicio += 1
            if ocorrencia.status == "Aberto":
                return ocorrencia
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


class MaxHeapPrioridade:
    def __init__(self):
        self._dados = []

    def inserir(self, ocorrencia):
        self._dados.append(ocorrencia)
        self._subir(len(self._dados) - 1)

    def extrair_aberta(self):
        while self._dados:
            maior = self._extrair_maior()
            if maior.status == "Aberto":
                return maior
        return None

    def _extrair_maior(self):
        if len(self._dados) == 1:
            return self._dados.pop()

        maior = self._dados[0]
        self._dados[0] = self._dados.pop()
        self._descer(0)
        return maior

    def _tem_maior_prioridade(self, a, b):
        if a.prioridade != b.prioridade:
            return a.prioridade > b.prioridade
        return a.ordem_chegada < b.ordem_chegada

    def _subir(self, indice):
        while indice > 0:
            pai = (indice - 1) // 2
            if not self._tem_maior_prioridade(self._dados[indice], self._dados[pai]):
                break
            self._dados[indice], self._dados[pai] = self._dados[pai], self._dados[indice]
            indice = pai

    def _descer(self, indice):
        tamanho = len(self._dados)
        while True:
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2
            maior = indice

            if esquerda < tamanho and self._tem_maior_prioridade(self._dados[esquerda], self._dados[maior]):
                maior = esquerda
            if direita < tamanho and self._tem_maior_prioridade(self._dados[direita], self._dados[maior]):
                maior = direita
            if maior == indice:
                break

            self._dados[indice], self._dados[maior] = self._dados[maior], self._dados[indice]
            indice = maior


class HashOcorrencias:
    def __init__(self, tamanho=31):
        self._tamanho = tamanho
        self._baldes = [[] for _ in range(tamanho)]

    def inserir(self, chave, ocorrencia):
        chave_normalizada = self._normalizar(chave)
        indice = self._hash(chave_normalizada)
        self._baldes[indice].append((chave_normalizada, ocorrencia))

    def buscar(self, chave):
        chave_normalizada = self._normalizar(chave)
        indice = self._hash(chave_normalizada)
        resultados = []
        ids_vistos = set()

        for chave_salva, ocorrencia in self._baldes[indice]:
            if chave_salva == chave_normalizada and ocorrencia.id not in ids_vistos:
                resultados.append(ocorrencia)
                ids_vistos.add(ocorrencia.id)

        return resultados

    def _hash(self, chave):
        total = 0
        for caractere in chave:
            total = (total * 31 + ord(caractere)) % self._tamanho
        return total

    def _normalizar(self, chave):
        return chave.strip().lower()
