import os
import sys

from armazenamento import carregar_estado, salvar_estado
from sistema import SistemaOcorrencias

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def formatar_ocorrencia(ocorrencia):
    return (
        f"ID: {ocorrencia.id} | Nome: {ocorrencia.nome} | Tipo: {ocorrencia.tipo} | "
        f"Prioridade: {ocorrencia.prioridade} | Ordem: {ocorrencia.ordem_chegada} | "
        f"Status: {ocorrencia.status}"
    )


def imprimir_ocorrencia_detalhada(ocorrencia):
    print(f"ID: {ocorrencia.id}")
    print(f"Nome: {ocorrencia.nome}")
    print(f"Tipo: {ocorrencia.tipo}")
    print(f"Descrição: {ocorrencia.descricao}")
    print(f"Prioridade: {ocorrencia.prioridade}")
    print(f"Ordem de chegada: {ocorrencia.ordem_chegada}")
    print(f"Status: {ocorrencia.status}")


def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        try:
            return int(valor)
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_prioridade():
    print("Prioridade: 1 = baixa, 5 = crítica.")
    while True:
        prioridade = ler_inteiro("Prioridade (1 a 5): ")
        if 1 <= prioridade <= 5:
            return prioridade
        print("Prioridade deve estar entre 1 e 5.")


def ler_texto_obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Esse campo não pode ficar vazio.")


def escolher_tipo_ocorrencia():
    print("Tipo da ocorrência:")
    print("1 - Laboratório")
    print("2 - Documento")
    print("3 - Suporte técnico")
    print("4 - Reserva de sala")
    print("5 - Equipamento")
    print("6 - Outro")

    while True:
        escolha = input("Escolha o tipo: ").strip()
        if escolha == "1":
            return "Laboratório"
        if escolha == "2":
            return "Documento"
        if escolha == "3":
            return "Suporte técnico"
        if escolha == "4":
            return "Reserva de sala"
        if escolha == "5":
            return "Equipamento"
        if escolha == "6":
            return ler_texto_obrigatorio("Informe o tipo da ocorrência: ")
        print("Opção inválida.")


def cadastrar_pelo_menu(sistema):
    print("\n--- Cadastrar ocorrência ---")
    nome = ler_texto_obrigatorio("Nome do solicitante: ")
    tipo = escolher_tipo_ocorrencia()
    descricao = ler_texto_obrigatorio("Descrição da ocorrência: ")
    prioridade = ler_prioridade()

    try:
        ocorrencia = sistema.cadastrar(nome, tipo, descricao, prioridade)
        print("Ocorrência cadastrada com sucesso:")
        print(formatar_ocorrencia(ocorrencia))
    except ValueError as erro:
        print(f"Erro: {erro}")


def listar_todas_pelo_menu(sistema):
    print("\n--- Lista geral ---")
    ocorrencias = sistema.listar_todas()
    if not ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return
    for ocorrencia in ocorrencias:
        print(formatar_ocorrencia(ocorrencia))


def atender_fila_pelo_menu(sistema):
    print("\n--- Atendimento por ordem de chegada ---")
    ocorrencia = sistema.atender_por_chegada()
    if ocorrencia is None:
        print("Nenhuma ocorrência aberta na fila.")
        return
    print("Ocorrência atendida:")
    imprimir_ocorrencia_detalhada(ocorrencia)


def atender_prioridade_pelo_menu(sistema):
    print("\n--- Atendimento por prioridade ---")
    ocorrencia = sistema.atender_por_prioridade()
    if ocorrencia is None:
        print("Nenhuma ocorrência aberta na heap.")
        return
    print("Ocorrência atendida:")
    imprimir_ocorrencia_detalhada(ocorrencia)


def buscar_id_pelo_menu(sistema):
    print("\n--- Buscar por ID ---")
    id_ocorrencia = ler_inteiro("Digite o ID: ")
    ocorrencia = sistema.buscar_por_id(id_ocorrencia)
    if ocorrencia is None:
        print("Ocorrência não encontrada.")
        return
    imprimir_ocorrencia_detalhada(ocorrencia)


def buscar_hash_pelo_menu(sistema):
    print("\n--- Buscar por nome ou tipo ---")
    chave = input("Digite o nome ou tipo: ").strip()
    resultados = sistema.buscar_por_nome_ou_tipo(chave)
    if not resultados:
        print("Nenhuma ocorrência encontrada para essa chave.")
        return
    for ocorrencia in resultados:
        print(formatar_ocorrencia(ocorrencia))


def ordenar_pelo_menu(sistema):
    print("\n--- Ordenação manual ---")
    print("1 - ID crescente")
    print("2 - Prioridade decrescente")
    print("3 - Nome crescente")
    escolha = input("Escolha o criterio: ").strip()
    if escolha == "1":
        campo = "id"
    elif escolha == "2":
        campo = "prioridade"
    elif escolha == "3":
        campo = "nome"
    else:
        print("Opção inválida.")
        return

    ocorrencias = sistema.ordenar_ocorrencias(campo)
    if not ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return
    for ocorrencia in ocorrencias:
        print(formatar_ocorrencia(ocorrencia))


def historico_pelo_menu(sistema):
    print("\n--- Histórico de ações ---")
    historico = sistema.ver_historico()
    if not historico:
        print("Histórico vazio.")
        return
    for indice, acao in enumerate(historico, start=1):
        print(f"{indice}. {acao}")


def desfazer_pelo_menu(sistema):
    print("\n--- Desfazer última ação ---")
    resultado = sistema.desfazer_ultima_acao()
    if resultado is None:
        print("Nenhuma ação para desfazer.")
        return
    print(resultado)


def limpar_tela():
    if sys.stdin.isatty() and sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def pausar():
    if sys.stdin.isatty():
        input("\nPressione Enter para voltar ao menu...")


def exibir_menu():
    print("\n===== SISTEMA DE OCORRÊNCIAS ACADÊMICAS =====")
    print("1 - Cadastrar ocorrência")
    print("2 - Listar todas as ocorrências")
    print("3 - Atender próxima ocorrência pela fila")
    print("4 - Atender ocorrência de maior prioridade")
    print("5 - Buscar ocorrência por ID")
    print("6 - Buscar ocorrências por nome ou tipo")
    print("7 - Ordenar ocorrências")
    print("8 - Ver histórico de ações")
    print("9 - Desfazer última ação")
    print("0 - Sair")


def executar_menu():
    sistema = carregar_estado()

    while True:
        limpar_tela()
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            salvar_estado(sistema)
            print("Encerrando o sistema.")
            break

        if escolha == "1":
            cadastrar_pelo_menu(sistema)
        elif escolha == "2":
            listar_todas_pelo_menu(sistema)
        elif escolha == "3":
            atender_fila_pelo_menu(sistema)
        elif escolha == "4":
            atender_prioridade_pelo_menu(sistema)
        elif escolha == "5":
            buscar_id_pelo_menu(sistema)
        elif escolha == "6":
            buscar_hash_pelo_menu(sistema)
        elif escolha == "7":
            ordenar_pelo_menu(sistema)
        elif escolha == "8":
            historico_pelo_menu(sistema)
        elif escolha == "9":
            desfazer_pelo_menu(sistema)
        else:
            print("Opção inválida.")
        pausar()


def executar_demo():
    sistema = SistemaOcorrencias()
    sistema.cadastrar("Ana Souza", "Documento", "Solicitação de histórico", 2)
    sistema.cadastrar("Maria Lima", "Laboratório", "Computador não liga", 5)
    sistema.cadastrar("João Pedro", "Equipamento", "Empréstimo de notebook", 3)

    print("DEMO - Sistema de Ocorrências Acadêmicas")
    print("\n1) Listagem após cadastros")
    for ocorrencia in sistema.listar_todas():
        print(formatar_ocorrencia(ocorrencia))

    print("\n2) Busca por ID usando árvore")
    imprimir_ocorrencia_detalhada(sistema.buscar_por_id(2))

    print("\n3) Busca por tipo usando hash table")
    for ocorrencia in sistema.buscar_por_nome_ou_tipo("Laboratório"):
        print(formatar_ocorrencia(ocorrencia))

    print("\n4) Atendimento por fila")
    imprimir_ocorrencia_detalhada(sistema.atender_por_chegada())

    print("\n5) Atendimento por prioridade")
    imprimir_ocorrencia_detalhada(sistema.atender_por_prioridade())

    print("\n6) Ordenação manual por ID")
    for ocorrencia in sistema.ordenar_ocorrencias("id"):
        print(formatar_ocorrencia(ocorrencia))

    print("\n7) Histórico pela pilha")
    for acao in sistema.ver_historico():
        print(acao)

    print("\n8) Desfazer atendimento por prioridade")
    print(sistema.desfazer_ultima_acao())
    imprimir_ocorrencia_detalhada(sistema.buscar_por_id(2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        executar_demo()
    else:
        executar_menu()
