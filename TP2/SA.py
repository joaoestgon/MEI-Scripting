
from cmath import exp
from netrc import NetrcParseError
import requests
import pandas
from bs4 import BeautifulSoup
import numpy as np
import re
import matplotlib.pyplot as plt



general ={}

df_exp = pandas.read_csv('expressions.csv')
expW = df_exp['word']
expS = df_exp['sentiment']

df_mult = pandas.read_csv('multip.csv')
multW = df_mult['word']
multS = df_mult['sentiment']

df_words = pandas.read_csv('words.csv')
wordW = df_words['word']
wordS = df_words['sentiment']

#Função que, sabendo o dataset, extrai o tipo de sentimento associado
#0 - expressões, 1 - , 2 - palavras
def getSentiment(position, type):
    if type==0:
        subj = expS[position]
    elif type==1:
        subj = multS[position]
    elif type==2:
        subj = wordS[position]
    if  subj > 0 :
        return 'bom'
    elif subj < 0:
        return 'mau'
    else:
        return 'neutro'

def catch_expressions(sentence):
    new_sentence = sentence
    for i in range(len(df_exp)):
        ans = re.findall(expW[i], sentence)
        if ans:
            for an in ans:
                new_sentence = new_sentence.replace(an, '')
                #obter o tipo de sentimento em função do valor
                sent = getSentiment(i, 0)
                #adicionar ao neg, pos ou neutro
                if sentence in general:
                    general[sentence][sent].append(expS[i])
                else:
                    general[sentence][sent]= [expS[i]]
    return new_sentence    


def catch_mult(original, new_sentence):
    for i in range(len(df_mult)):
        ans = re.findall(multW[i]+r'\s\w+', new_sentence)
        for an in ans:
            new_sentence = new_sentence.replace(an, '')
            sent = getSentiment(i, 1)
                #adicionar ao neg, pos ou neutro
            if original in general:
                general[original][sent].append(multS[i])
            else:
                general[original][sent]= [multS[i]]
    return new_sentence    

def catch_words(original, new_sentence):
    for i in range(len(df_words)):
        ans = re.findall(wordW[i], new_sentence)
        for an in ans:
            new_sentence = new_sentence.replace(an, '')
            sent = getSentiment(i, 2)
                #adicionar ao neg, pos ou neutro
            if original in general:
                general[original][sent].append(wordS[i])
            else:
                general[original][sent]= [wordS[i]]
    return new_sentence  

def diagram():
    pos = 0
    neg= 0
    net = 0
    for entry in general:
        if general[entry]['total'] == 'POSITIVO':
            pos += 1
        elif general[entry]['total'] == 'NEGATIVO':
            neg += 1
        elif general[entry]['total'] == 'NEUTRO':
            net += 1



# Pie chart, where the slices will be ordered 
# and plotted counter-clockwise:
    labels = 'Positivo', 'Negativo', 'Neutro'
    sizes = [pos, neg, net]

    distance = 0.2
    separate = (distance, distance, distance)
    plt.figure()
    plt.pie(sizes, labels=labels, explode=separate, autopct='%1.1f%%')
    # Equal aspect ratio ensures that 
    # pie is drawn as a circle.
    plt.axis('equal')  
    plt.title('Análise de Sentimentos das Notícias do dia')
    plt.show()


def process_Sentiment():
    for entry in general:

        total = sum(int(v) for v in general[entry]['bom']) + sum(int(v) for v in general[entry]['neutro']) + sum(int(v) for v in general[entry]['mau'])
        total_sents = (len(general[entry]['bom']+general[entry]['neutro']+general[entry]['mau']))
        total_mean = 0
        pos=0
        neg=0
        neut = 0
        if total_sents> 0 :
            total_mean = total/ total_sents
            pos +=1
        if total_mean < 0:
            SENT = 'NEGATIVO'
            neg+=1
        elif total_mean >0:
            SENT = 'POSITIVO'
            neut+=1
        elif total_mean== 0:
            SENT ='NEUTRO'
        general[entry]['total'] = SENT
        print(f'Para o Título: \n\t"{entry}"\n O sentimento geral associado é {total}, com uma média de {total_mean}, ou seja, {SENT}.\n\n')

def analyseSents():
    url='https://www.publico.pt/online'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    #Retirar todas as headlines do site para analisar os sentimentos
    headlines = soup.find('body').find_all('h4', 'headline')
    #headlines = ['isto é um ponto forte muito lindo, vamos testar outro ponto forte', 'isto é outro ponto fraco', 'que deixa muito a desejar', 'que coisa muito linda']

    for x in headlines: 
        x = x.text.strip()
        general[x] = {'bom': [], 'mau': [], 'neutro': [], 'total': ''}
        #x.text.strip()
        x1 = catch_expressions(x)
        x2 = catch_mult(x, x1)
        x3 = catch_words(x, x2)

    process_Sentiment()
    diagram()

analyseSents() 
