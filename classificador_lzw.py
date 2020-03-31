# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:47:34 2020

@author: Yuri Oliveira
"""

import numpy as np
import PIL
import matplotlib.pyplot as plt
import time
import random

#le todas as imagens de uma determinada pessoa na base de dados ORL
def leImagensPessoa(nPessoa):
    listaImagens = []
    for j in range(1,numeroImagensPessoa + 1):       
        listaImagens.append(PIL.Image.open('C:/Users/Yuri Oliveira/Desktop/orl_faces/s'+ str(nPessoa) +'/'+ str(j) +'.pgm'))
    return listaImagens
    
#transforma a imagem numa string
def transformaImgEmString(imagem):
    mensagem = ""
    for y in range(112):
        for x in range(92):
            mensagem = mensagem + chr(imagem.getpixel((x,y)))
    return mensagem

#verifica se a imagem da pessoa recebeu a classificacao correta, 1 pra sim e 0 pra nao
def classificaImagem(pessoa, k):
    saidas = saidas_classificacao[((k-9)*(numeroPessoas**2))+(numeroPessoas*(pessoa-1)):((k-9)*(numeroPessoas**2))+(numeroPessoas*(pessoa))]
    tamanhoSaidas = [len(saida) for saida in saidas]
    menorTamanho = min(tamanhoSaidas)
    indice = tamanhoSaidas.index(menorTamanho)
    print("indice: " + str(indice))
    if indice == (pessoa - 1):
        return 1
    else:
        print("classificacao incorreta da pessoa: " + str(pessoa))
        return 0

#Verifica se existe o simbolo no dicionario
#Retorna o seu indice, caso exista.
def existeNoDic(simbolo):
    if simbolo in dic:
        return dic.index(simbolo)
    return -1

def LZW(k, mensagem, dic):
    #pega o tempo de execucao
    #tempo_inicial = time.time()
    #Saida Codificada
    saida = []
    #variaveis auxiliar
    I = ''
    i=0    
    for i in range(len(mensagem)):    
        c = mensagem[i]
        #verifica se existe o simbolo atual e o proximo no dicionario
        if existeNoDic(I+c) != -1:
            I = I+c
        #senao existir, adiciona o indice do simbolo atual na saida e
        #adiciona no dicionario o simbolo atual + proximo como novo indice
        else:
            saida.append(existeNoDic(I))
            #adiciona o novo simbolo no dicionario (se ele não estiver cheio)
            if len(dic) < (2**k):
                dic.append(I+c)
            I = c
        #Enquanto nao pegar todos os simbolos, continua rodando o looping
        if (i+1) < len(mensagem):
            continue
        else:
            saida.append(existeNoDic(I))
        
    return saida

'''
    Inicio do Treinamento
'''
#parametros do algoritmo
numeroPessoas = 40  #numero de pessoas da base de dados que quer testar
numeroImagensPessoa = 10  #numero de imagens por pessoa
kMax = 17 #faz o k variar de 9 a 16


#Iniciando o dicionario
dic_tamanho = 256
dicionario = [chr(i) for i in range(dic_tamanho)]

tempos_k = [] #variavel que guarda os tempos de execução da criação dos dicionarios em cada K
saidas = []   #variavel que guarda as saidas geradas por cada imagem. 40 pessoas x 9 imagens = 360 saidas
dicionarios = []  #variavel que guarda o dicionario das 40 pessoas, um por pessoa
listaImagensTeste = [random.randint(0,9) for i in range(numeroPessoas)]  #cria uma lista com os indices das imagens de teste de cada pessoa

#faz para K valendo de 9 a 16
#gera todos os dicionarios do projeto (um dicionario por pessoa)
for k in range(9,kMax):
    #pega o tempo de execucao
    tempo_inicial = time.time()
    #percorre todas as pessoas
    for pessoa in range(1, numeroPessoas+1):
        listaImagens = leImagensPessoa(pessoa)
        del listaImagens[listaImagensTeste[pessoa-1]]  #deleta a imagem que será utilizada como teste
        dic = dicionario[0:] #para cada pessoa, "zera" o dicionario
        #percorre as 9 faces de cada pessoa
        for face in range(numeroImagensPessoa-1):
            imagem = listaImagens[face]
            mensagem = transformaImgEmString(imagem)
            saida = LZW(k, mensagem, dic)
            #saidas.append(saida)
        dicionarios.append(dic)
    print("tempo: " + str(time.time() - tempo_inicial))
    tempos_k.append(time.time() - tempo_inicial)
'''            
    Fim do Treinamento
    
    Inicio da classificação
''' 
    
saidas_classificacao = [] #guarda todas as saidas que foram geradas pelo laço abaixo
tempos_k_classificacao = []

#compara a foto de teste de cada pessoa com todos os dicionarios existentes (1 dicionario por pessoa)
for k in range(9,kMax):
    #pega o tempo de execucao
    tempo_inicial = time.time()
    print("utilizando k: " + str(k))
    for pessoa in range(1, numeroPessoas+1):
        print("pessoa: " + str(pessoa))
        listaImagens = leImagensPessoa(pessoa)
        imagem = listaImagens[listaImagensTeste[pessoa-1]]
        mensagem = transformaImgEmString(imagem)
        for d in range((k-9)*numeroPessoas, ((k-9)*numeroPessoas) + numeroPessoas):
            print("utilizando dicionario: " + str(d))
            dic = dicionarios[d]
            saida = LZW(k, mensagem, dic)
            saidas_classificacao.append(saida)
    print("tempo: " + str(time.time() - tempo_inicial))
    tempos_k_classificacao.append(time.time() - tempo_inicial)

qtdeAcertos = [] #lista que guarda a quantidade de acertos do algoritmo para cada K

#verifica quantos acertos a máquina teve (para todos os Ks)
for k in range(9,kMax):
    print("K valendo: " + str(k))
    classificacaoAcertos = 0
    for pessoa in range(1, numeroPessoas+1):
        resultado = classificaImagem(pessoa, k)
        if resultado == 1:
            print("classificacao correta da pessoa: " + str(pessoa))
            classificacaoAcertos += 1
    print("Quantidade de acertos: " + str(classificacaoAcertos))
    qtdeAcertos.append(classificacaoAcertos)
    
#taxa de acertos (em porcentagem)
qtdeAcertos = [100*(acertos/numeroPessoas) for acertos in qtdeAcertos]

#coloca tempo da classificacao em minutos
tempos_k = [tempo/60 for tempo in tempos_k]

#graficos de tempo de processamento do algoritmo
plt.figure()
plt.title('tempo de processamento do treinamento x K')
plt.ylabel('Tempo de processamento (minutos)')
plt.xlabel('K')
plt.plot(list(range(9,17)), tempos_k)
plt.grid(True)

#grafico de taxa de acertos do algoritmo
plt.figure()
plt.title('taxa de acertos x K')
plt.ylabel('Taxa de acertos')
plt.xlabel('K')
plt.plot(list(range(9,17)), qtdeAcertos)
plt.grid(True)

#coloca tempo da classificacao em minutos
tempos_k_classificacao = [tempo/60 for tempo in tempos_k_classificacao]

#graficos de tempo de processamento do algoritmo
plt.figure()
plt.title('tempo de processamento x K')
plt.ylabel('Tempo de processamento (minutos)')
plt.xlabel('K')
plt.plot(list(range(9,17)), tempos_k_classificacao)
plt.grid(True)



#image = PIL.Image.open('C:/Users/Yuri Oliveira/Desktop/orl_faces/s1/3.pgm')
#mostra a imagem
#for imagem in listaImagens:
#    plt.figure()
#    plt.imshow(imagem)
