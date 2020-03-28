# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:47:34 2020

@author: Yuri Oliveira
"""

import numpy as np
import PIL
import matplotlib.pyplot as plt

#treina com 9 imagens de cada pessoa
#Gera o dicionario de cada pessoa e guarda numa variavel
#

def leImagensDeTreinamento(nPessoa):
        for j in range(1,numeroImagensPessoa + 1):       
           listaImagens.append(PIL.Image.open('C:/Users/Yuri Oliveira/Desktop/orl_faces/s'+ str(nPessoa) +'/'+ str(j) +'.pgm'))

#transforma a imagem numa string
def transformaImgEmString(imagem):
    mensagem = ""
    for y in range(112):
        for x in range(92):
            mensagem = mensagem + chr(imagem.getpixel((x,y)))
    return mensagem

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

listaImagens = []
numeroPessoas = 40
numeroImagensPessoa = 10

'''
    Inicio do Treinamento
'''
#LZW_WikiPedia

#Iniciando o dicionario
dic_tamanho = 256
dicionario = [chr(i) for i in range(dic_tamanho)]

tempos_k = []
saidas = []   #variavel que guarda as saidas geradas por cada imagem. 40 pessoas x 9 imagens = 360 saidas
dicionarios = []  #variavel que guarda o dicionario das 40 pessoas, um por pessoa
#faz para K valendo de 9 a 16
for k in range(9,10):
    
    #percorre todas as pessoas
    for pessoa in range(1, 3+1):
        listaImagens = []  
        leImagensDeTreinamento(pessoa)
        dic = dicionario[0:] #para cada pessoa, "zera" o dicionario
        #percorre as 9 faces de cada pessoa
        for face in range(numeroImagensPessoa):
            imagem = listaImagens[face]
            mensagem = transformaImgEmString(imagem)
            saida = LZW(k, mensagem, dic)
            saidas.append(saida)
        dicionarios.append(dic)
            #tempos_k.append(time.time() - tempo_inicial)
'''            
    Fim do Treinamento
    
    Inicio da classificação
''' 

#testando a ultima imagem de uma pessoa
listaImagens = []
leImagensDeTreinamento(2)
imagem = listaImagens[9]
 
#image = PIL.Image.open('C:/Users/Yuri Oliveira/Desktop/orl_faces/s1/3.pgm')
#mostra a imagem
#for imagem in listaImagens:
#    plt.figure()
#    plt.imshow(imagem)
#plt.imshow(imagem)