import os
import requests
from deep_translator import GoogleTranslator

os.system('cls' if os.name == 'nt' else 'clear')

def traduzir_para_portugues(texto):
    return GoogleTranslator(source='en', target='pt').translate(texto)

def solicitacao_de_conselhos(qtde):
    contar = 0
    dicio = {}  
    traco = '  ----------------------------  '

    while contar < qtde:
        pedido_url = "https://api.adviceslip.com/advice"
        resposta = requests.get(pedido_url)
        id = resposta.json()['slip']

        conselho_original = id['advice']

        print(f'\nConselho Original (Inglês): {conselho_original}')
        print(f'{traco}Id do Conselho: {str(id["id"])}\n')

        print("\n--- Você quer traduzir este conselho para português? --- \n")
        traduzir = input().strip().upper()

        if traduzir == 'SIM':
            conselho_traduzido = traduzir_para_portugues(conselho_original)
            print(f'\nConselho Traduzido (Português): {conselho_traduzido}')
            dicio[str(id['id'])] = conselho_traduzido
        else:
            dicio[str(id['id'])] = conselho_original

        # Perguntar se deseja guardar o conselho
        print("\n--- Você quer guardar este conselho? --- \n")
        guardar = input().strip().upper()

        if guardar == 'SIM':
            guardar_conselho(dicio.popitem())
        
        contar += 1

def guardar_conselho(tupla):
    with open("conselhos.txt", 'a') as arq:
        arq.write(tupla[0] + ' --- ' + tupla[1] + '\n')

def resgatar_conselho(id):
    with open("conselhos.txt", 'r') as arq:
        for leitura in arq:
            if leitura.startswith(id + ' '):
                print(f"O conselho requerido é: {leitura[len(id) + 1:].strip()}")
                print("                     ----------------- Este é um bom conselho :) -------------")
                return
        print("Conselho não encontrado.")

def mostrar_todos_conselhos():
    print("\n--- Todos os Conselhos Armazenados ---\n")
    try:
        with open("conselhos.txt", 'r') as arq:
            conteudo = arq.readlines()
            if not conteudo:
                print("Nenhum conselho armazenado ainda.")
            else:
                for linha in conteudo:
                    print(linha.strip())
    except FileNotFoundError:
        print("Nenhum arquivo encontrado. Nenhum conselho armazenado ainda.")

print("----- Bem-vindo ao Orientador de Conselhos! -----")
print("Quantos conselhos você deseja receber?\n")

conselhos = int(input())

with open("conselhos.txt", 'w'):
    pass  # Limpa o arquivo antes de começar

solicitacao_de_conselhos(conselhos)

while True:
    print("\n--- Escolha uma das opções abaixo ---")
    print("1. Resgatar um conselho pelo ID")
    print("2. Mostrar todos os conselhos armazenados")
    print("3. Sair")
    escolha = input("\nDigite sua escolha: ").strip()

    if escolha == '1':
        print("\nDigite o ID do conselho que deseja resgatar: ")
        id = input()
        resgatar_conselho(id)
    elif escolha == '2':
        mostrar_todos_conselhos()
    elif escolha == '3':
        print("Obrigado por usar o Orientador de Conselhos. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")
