# Sistema de Ocorrências Acadêmicas

Aplicação de linha de comando para gerenciar ocorrências acadêmicas usando estruturas de dados em memória.

## Como executar

```bat
python main.py
```

Para rodar uma demonstração automática:

```bat
python main.py --demo
```

## Organização dos arquivos

- `main.py`: menu textual, leitura de dados e exibição no terminal.
- `modelos.py`: modelo da ocorrência acadêmica.
- `estruturas.py`: pilha, fila, árvore binária, heap e hash table.
- `sistema.py`: regras de cadastro, atendimento, busca, histórico e ordenação.

## Menu principal

```text
1 - Cadastrar ocorrência
2 - Listar todas as ocorrências
3 - Atender próxima ocorrência pela fila
4 - Atender ocorrência de maior prioridade
5 - Buscar ocorrência por ID
6 - Buscar ocorrências por nome ou tipo
7 - Ordenar ocorrências
8 - Ver histórico de ações
9 - Desfazer última ação
0 - Sair
```

No cadastro, o sistema gera o ID automaticamente a partir de `1`, define a ordem de chegada e cria a ocorrência com status `Aberto`. O usuário informa nome, escolhe o tipo em uma lista, descreve a ocorrência e informa a prioridade.

Depois de executar uma opção, o sistema mostra o resultado e espera Enter para voltar ao menu.

A opção de desfazer remove a última ação da pilha. Se a última ação for um atendimento, a ocorrência volta para `Aberto`. Se for um cadastro, a ocorrência cadastrada é removida. Listagem, busca e ordenação não entram no desfazer porque não alteram os dados do sistema.

## Estruturas usadas

- Lista: armazena todas as ocorrências cadastradas.
- Fila: atende as ocorrências abertas por ordem de chegada.
- Pilha: guarda o histórico de cadastros e atendimentos.
- Árvore binária de busca: localiza uma ocorrência pelo ID.
- Heap máxima: atende primeiro a ocorrência aberta de maior prioridade.
- Hash table: busca ocorrências por nome do solicitante ou tipo.
- Ordenação manual: usa bubble sort para ordenar por ID, prioridade ou nome.

## Consistencia dos dados

As ocorrências ficam em memória. Quando uma ocorrência é atendida, ela continua na lista geral, mas seu status muda para `Atendido`. A fila e a heap ignoram ocorrências que já foram atendidas por outro critério.

## Evidencia

O arquivo `evidencias/demo.txt` contém a saída de uma execução automática mostrando cadastro, listagem, busca por ID, busca por tipo, atendimento por fila, atendimento por prioridade, ordenação e histórico.
