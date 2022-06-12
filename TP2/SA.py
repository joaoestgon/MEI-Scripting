
from cmath import exp
import requests
import pandas
from bs4 import BeautifulSoup
import numpy as np
import re

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

def process_Sentiment():
    for entry in general:
        total = sum(int(v) for v in general[entry]['bom']) + sum(int(v) for v in general[entry]['neutro']) + sum(int(v) for v in general[entry]['mau'])
        total_mean = total/ (len(general[entry]['bom']+general[entry]['neutro']+general[entry]['mau']))
        if total_mean < 0:
            SENT = 'NEGATIVO'
        elif total_mean >0:
            SENT = 'POSITIVO'
        elif total_mean== 0:
            SENT ='NEUTRO'
        print(f'Para a frase: \n"{entry}"\n o sentimento geral associado é {total}, com uma média de {total_mean}, ou seja, {SENT}.\n\n')

def analyseSents():
    url='https://www.publico.pt/online'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    #Retirar todas as headlines do site para analisar os sentimentos
    #headlines = soup.find('body').find_all('h4', 'headline')
    headlines = ['isto é um ponto forte muito lindo, vamos testar outro ponto forte', 'isto é outro ponto fraco', 'que deixa muito a desejar', 'que coisa muito linda']

    for x in headlines: 
        x = x.strip()
        general[x] = {'bom': [], 'mau': [], 'neutro': []}
        #x.text.strip()
        x1 = catch_expressions(x)
        x2 = catch_mult(x, x1)
        x3 = catch_words(x, x2)

    process_Sentiment()

analyseSents() 
'''
unwanted = ['BBC World News TV', 'BBC World Service Radio', 'News daily newsletter', 'Mobile app', 'Get in touch']
news = []
neutral = []
bad = []
good = []
for x in headlines:
    if x.text.strip() not in unwanted and x.text.strip() not in news:
        news.append(x.text.strip())
        for i in range(len(df['n'])):
            if sen[i] in x.text.strip().lower():
                if cat[i] == 0:
                    bad.append(x.text.strip().lower())
                else:
                    good.append(x.text.strip().lower())

badp = len(bad)
goodp = len(good)
nep = len(news) - (badp + goodp)
print('Scraped headlines: '+ str(len(news)))
print('Headlines with negative sentiment: ' + str(badp) + '\nHeadlines with positive sentiment: ' + str(goodp) + '\nHeadlines with neutral sentiment: ' + str(nep))

finalAnal = (badp * -1 + goodp * 1 )/(badp+goodp+nep)

print("Média de sentimentos das notícias: ", finalAnal)


'''