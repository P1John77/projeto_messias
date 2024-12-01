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
    with open("teste_1.txt", 'a') as arq:
        arq.write(tupla[0] + ' --- ' + tupla[1] + '\n')


def resgatar_conselho(id):
    with open("teste_1.txt", 'r') as arq:
        for leitura in arq:
            if leitura.startswith(id + ' '):
                print(f"O conselho requerido é: {leitura[len(id) + 1:].strip()}")
                print("                     ----------------- Este é um bom conselho :) -------------")
                return
        print("Conselho não encontrado.")


print("----- Bom dia! Seja bem-vindo à Cachaçaria do Seu Zé! -------- \n")
print("----- Depois de uma boa, nada melhor do que buscar orientação na vida, não é mesmo? ----- :) :)\n")
print("----- Diga quantos conselhos deseja -------\n ")

conselhos = int(input())


with open("teste_1.txt", 'w'):
    pass


solicitacao_de_conselhos(conselhos)


print("---- Você deseja resgatar algum conselho? ------ \n")
s = input('\n')

if s.upper() == 'SIM':
    print("\nDigite o id \n")
    id = input()
    resgatar_conselho(str(id))
