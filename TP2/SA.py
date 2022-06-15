
from cmath import exp
from netrc import NetrcParseError
#import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import sys
import spacy
import nltk
load_model = spacy.load("pt_core_news_sm", disable = ['parser','ner'])
all_stopwords =  nltk.corpus.stopwords.words("portuguese")

general ={}

df_exp = pd.read_csv('exp.csv')
expW = df_exp['word']
expS = df_exp['sentiment']

df_mult = pd.read_csv('mult.csv')
multW = df_mult['word']
multS = df_mult['sentiment']


'''
#Transformar o dataset num csv
dataframe1 = pd.read_csv("SentiLex.txt", delimiter=';') 
dataframe1.to_csv('SentiLex.csv', 
                  index = None, header=['word', 'sent'])'''

df_words = pd.read_csv("SentiLex.csv")
wordW = df_words['word']
wordS = df_words['sent']



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

def catch_expressions(original, sentence):
    new_sentence = sentence
    for i in range(len(df_exp)):
        ans = re.findall(expW[i], sentence)
        if ans:
            for an in ans:
                new_sentence = new_sentence.replace(an, '')
                #obter o tipo de sentimento em função do valor
                sent = getSentiment(i, 0)
                #adicionar ao neg, pos ou neutro
                if original in general:
                    general[original][sent].append(expS[i])
                else:
                    general[original][sent]= [expS[i]]
    return new_sentence    


def catch_mult(original, new_sentence):
    for i in range(len(df_mult)):
        word_comp = re.findall(multW[i]+r'\s(\w+)', new_sentence)
        for an in word_comp:
            for j in range(len(df_words)):
                if an == wordW[j]:
                    new_sentence = new_sentence.replace(multW[i] + ' ' +an, '')
                    sent = getSentiment(i, 1)
                        #adicionar ao neg, pos ou neutro
                    if original in general:
                        general[original][sent].append(multS[i]*wordS[j])
                    else:
                        general[original][sent]= [multS[i]*wordS[j]]

                    break
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
        print(f' 📜 → Para o Título: \n\t"{entry}"\n O sentimento geral associado é {total}, com uma média de {total_mean}, ou seja, {SENT}.\n\n')

def tolistString(blocks):
    b = []
    x = blocks.replace(r'\[|\]', '')
    res = re.findall(r'\'[^\']+\'\,?', x)
    for r in res:
        r = re.sub(r'\'\,|\'', '', r)
        b.append(r)
    return b


def lemmatization(texto):
    doc = load_model(texto)
    return(" ".join([token.lemma_ for token in doc]))


def remove_mystopwords(text):
    #fazer a tokenização por frases, para ser mais fácil
    f = nltk.sent_tokenize(text)
    tokens_filtered = []
    for sent in f:
        tokens = sent.split(" ")
        tokens_filtered += [word for word in tokens if not word in all_stopwords]
    return (" ").join(tokens_filtered)


def analyseSents(file):
    content = open(file, 'r').read()
    blocks = tolistString(content)
    for x in blocks: 
        general[x] = {'bom': [], 'mau': [], 'neutro': [], 'total': ''}
        #x.text.strip()
        x_lem = lemmatization(x)
        x1 = catch_expressions(x, x_lem)
        x2 = catch_mult(x, x1)
        x_WS = remove_mystopwords(x2)
        x3 = catch_words(x, x_WS)
 
    process_Sentiment()
    '''
    diagram()'''

analyseSents(sys.argv[1]) 


