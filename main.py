import os  # Importa funcionalidades do sistema operacional, como limpar a tela do terminal.
import requests  # Usado para fazer requisições HTTP, neste caso, para acessar a API de conselhos.
from deep_translator import GoogleTranslator  # Biblioteca para traduzir textos usando o Google Translate.

# Limpa o terminal: 'cls' para Windows, 'clear' para outros sistemas.
os.system('cls' if os.name == 'nt' else 'clear')

# Função que traduz um texto do inglês para o português.
def traduzir_para_portugues(texto):
    return GoogleTranslator(source='en', target='pt').translate(texto)

# Função principal para solicitar conselhos da API e gerenciar as respostas.
def solicitacao_de_conselhos(qtde):
    contar = 0  # Contador de conselhos recebidos.
    dicio = {}  # Dicionário para armazenar conselhos temporariamente.
    traco = '  ----------------------------  '  # Apenas uma linha decorativa.

    while contar < qtde:
        pedido_url = "https://api.adviceslip.com/advice"  # URL da API para conselhos.
        resposta = requests.get(pedido_url)  # Faz uma requisição GET para a API.
        id = resposta.json()['slip']  # Extrai o JSON retornado e obtém o conselho e seu ID.

        conselho_original = id['advice']  # Conselho em inglês.

        # Mostra o conselho original e seu ID no terminal.
        print(f'\nConselho Original (Inglês): {conselho_original}')
        print(f'{traco}Id do Conselho: {str(id["id"])}\n')

        # Pergunta se o usuário deseja traduzir o conselho.
        print("\n--- Você quer traduzir este conselho para português? --- \n")
        traduzir = input().strip().upper()

        if traduzir == 'SIM':
            # Traduz o conselho para português e exibe o resultado.
            conselho_traduzido = traduzir_para_portugues(conselho_original)
            print(f'\nConselho Traduzido (Português): {conselho_traduzido}')
            dicio[str(id['id'])] = conselho_traduzido
        else:
            # Armazena o conselho original sem traduzir.
            dicio[str(id['id'])] = conselho_original

        # Pergunta se o usuário deseja guardar o conselho.
        print("\n--- Você quer guardar este conselho? --- \n")
        guardar = input().strip().upper()

        if guardar == 'SIM':
            # Guarda o último conselho adicionado no dicionário em um arquivo.
            guardar_conselho(dicio.popitem())
        
        contar += 1  # Incrementa o contador de conselhos.

# Função que salva um conselho no arquivo "conselhos.txt".
def guardar_conselho(tupla):
    with open("conselhos.txt", 'a') as arq:  # Abre o arquivo em modo de anexação.
        arq.write(tupla[0] + ' --- ' + tupla[1] + '\n')  # Salva o ID e o conselho no arquivo.

# Função para buscar e exibir um conselho armazenado com base no ID.
def resgatar_conselho(id):
    with open("conselhos.txt", 'r') as arq:  # Abre o arquivo para leitura.
        for leitura in arq:  # Percorre cada linha do arquivo.
            if leitura.startswith(id + ' '):  # Verifica se a linha começa com o ID fornecido.
                print(f"O conselho requerido é: {leitura[len(id) + 1:].strip()}")
                print("                     ----------------- Este é um bom conselho :) -------------")
                return
        print("Conselho não encontrado.")  # Caso o ID não seja encontrado.

# Função para exibir todos os conselhos armazenados no arquivo.
def mostrar_todos_conselhos():
    print("\n--- Todos os Conselhos Armazenados ---\n")
    try:
        with open("conselhos.txt", 'r') as arq:  # Tenta abrir o arquivo para leitura.
            conteudo = arq.readlines()  # Lê todas as linhas.
            if not conteudo:
                print("Nenhum conselho armazenado ainda.")  # Caso o arquivo esteja vazio.
            else:
                for linha in conteudo:  # Exibe cada linha do arquivo.
                    print(linha.strip())
    except FileNotFoundError:
        print("Nenhum arquivo encontrado. Nenhum conselho armazenado ainda.")  # Caso o arquivo não exista.

# Mensagem inicial e solicitação de quantos conselhos o usuário deseja.
print("----- Bem-vindo ao Orientador de Conselhos! -----")
print("Quantos conselhos você deseja receber?\n")

conselhos = int(input())  # Recebe a quantidade de conselhos desejados do usuário.

with open("conselhos.txt", 'w'):  # Limpa o conteúdo do arquivo antes de começar.
    pass

# Inicia o processo de solicitação de conselhos.
solicitacao_de_conselhos(conselhos)

# Loop para gerenciar opções adicionais após receber conselhos.
while True:
    print("\n--- Escolha uma das opções abaixo ---")
    print("1. Resgatar um conselho pelo ID")
    print("2. Mostrar todos os conselhos armazenados")
    print("3. Sair")
    escolha = input("\nDigite sua escolha: ").strip()

    if escolha == '1':
        print("\nDigite o ID do conselho que deseja resgatar: ")
        id = input()  # Solicita o ID do conselho.
        resgatar_conselho(id)  # Chama a função de busca.
    elif escolha == '2':
        mostrar_todos_conselhos()  # Exibe todos os conselhos armazenados.
    elif escolha == '3':
        print("Obrigado por usar o Orientador de Conselhos. Até logo!")  # Sai do programa.
        break
    else:
        print("Opção inválida. Tente novamente.")  # Caso a escolha não seja válida.
