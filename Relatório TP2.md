# Tema 2 - Sentiment Analysis

## O que é Sentiment Analysis? 

Sentiment Analysis é uma técnica que permite analisar um pedaço de texto para determinar o sentimento por trás do mesmo. Por norma, combina machine learning e processamento de linguagem natural (NLP) para o conseguir. Através desta técnica, um programa consegue determinar se o sentimento associado a um pedaço de texto é positivo, negativo ou neutro. É uma técnica poderosa que tem aplicações empresariais importantes. como por exemplo, analisar o feedback de clientes. Depois de recolher esse feedback através de vários meios como o Twitter e o Facebook, uma empresa pode empregar algoritmos de Sentiment Analysis nesses excertos de texto para entender a atitude dos seus clientes em relação ao seu produto ou serviço.

## A nossa abordagem: Sistema Baseado em Regras

Ao contrário dos modelos automatizados, as abordagens baseadas em regras dependem de regras personalizadas para classificar os dados. Técnicas populares para este efeito incluem tokenização, parsing, cauling, entre outras. Uma vantagem dos sistemas baseados em regras é a capacidade de personalizção, podendo estes ser baseados em contextos mais específicos, desenvolvendo regras mais inteligentes.

## Projeto

O nosso projeto consiste no emprego de técnicas de sentiment analysis baseada em regras para analisar os títulos de notícias retiradas do site https://www.publico.pt/, procedendo depois ao tratamento dos dados resultantes dessa análise. Desta forma, é-nos possível tirar conclusões quanto à variação dos sentimentos dentro das próprias notícias, comparar sentimentos entre as várias notícias, para além de tecer padrões ao longo do tempo das mudanças nos sentimentos.

### 1. Tratamento do Dataset

O dataset utilizado para funcionar como dicionário de regras foi o SentiLex, sugerido pelos professores desta UC.
Para melhor adaptar o dataset às nossas necessidades, removemos as colunas que não interessavam e removemos algumas palavras cujo contexto não fazia sentido ou que achamos que iriam prejudicar a análise dos sentimentos.

### 2. Estratégia de Análise de Sentimentos

Começamos por definir os 3 principais tipos de sentimentos: bom, mau e neutro. A partir daí, aproveitamos o facto de que os sentimentos no dataset SentiLex estão cotados numa escala de [-1, 1] e utilizamos esta mesma escala nas nossas análises.

De seguida, ciramos um dataset adicional com palavras que classificamos como 'MULTIPLICADORAS' (ex.: muito, pouco, ...), visto que estas palavras aumentam ou diminuem o valor do sentimento da palavra que as procede.

** Fórmula: [Valor da Palavra Multiplicadora] x [Sentimento da Palavra] **

Como existem expressões cujas palavras individualmente possuem um sentimento diferente de quando estão combinadas numa mesma frase. Por isso, dividimos o dataset de modo a ter um dataset apenas para expressões e outro com todas as palavras individuais do SentiLex.
De modo a proceder a esta divisão, foram empregados os conhecimentos adquiridos na UC de SPLN, para desenvolver um script que faça essa divisão, visto que manualmente implicaria percorrer todas as entradas do SentiLex, procurar as expressões removê-las e colocá-las noutro dataset.

```
import csv
import re
import pandas as pd

# Função que procura todas alinhas do SentiLex.csv com espaços [\s]+ e as coloca numa lista de strings

def LerParaLista() :

    with open('SentiLex.csv', "r", encoding='utf-8') as file:
        data = file.read().splitlines()
        lista = []
        for row in data :
            if (re.search("[\s]+", row)) :
                lista.append(row)
        return (lista)

# Gera os csv de Expressões e Palavras

def GerarDocumentos(lista) :

    txt = open('exp.txt','w', encoding='utf-8')

    for elem in lista :    
        txt.write(elem + '\n')

    txt.close()

    #Transformar num csv
    dataframe1 = pd.read_csv("exp.txt", delimiter=',') 
    dataframe1.to_csv('Express.csv', index = None, header=['word', 'sent'])

    with open('SentiLex.csv', "r", encoding='utf-8') as inp :

        txt = open('tratado.txt','w', encoding='utf-8')
        
        for row in csv.reader(inp):
            
            #Tratamento das linhas para ficar igual ás do .csv
            row = str(row)
            row = re.sub(r'\[|\]', '', row)
            row = re.sub(r'\'', '', row)
            row = re.sub(r', ', ',', row)

            flag = 0
            
            # Se a expressão estiver na lista, não escreve no novo ficheiro, pois flga fica a 1
            
            for exp in lista :
                if (exp == row) :
                    flag = 1

            if(flag == 0) :
                #print('Escrever no ficheiro: ' + row)
                txt.write(row + '\n')

        txt.close()

    #Transformar num csv
    dataframe1 = pd.read_csv("tratado.txt", delimiter=',') 
    dataframe1.to_csv('SentiLex2.csv', index = None)

GerarDocumentos(LerParaLista())
```
