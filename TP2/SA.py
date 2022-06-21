
#import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import sys
import spacy
import nltk
import spacy
from spacy.lang.pt.examples import sentences 
import json
import numpy as np

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

nlp = spacy.load("pt_core_news_sm")
bom = nlp("bom")[0]
mau = nlp("bom")[0]


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


def process_Sentiment():
    for entry in general:
        total = sum(float(v) for v in general[entry]['bom']) + sum(float(v) for v in general[entry]['mau'])
        total_sents = (len(general[entry]['bom']) +len(general[entry]['neutro'])+ len(general[entry]['mau']))
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
        general[entry]['valor'] = total_mean
        print(f' 📜 → Para o Título: \n\t"{entry}"\n O sentimento total associado é {total_mean}, ou seja, {SENT}.\n\n')

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

def similarityWords(original, text):
    doc = nlp(text)
    for token1 in doc:
        similaridadeB = token1.similarity(bom)
        similaridadeM = token1.similarity(mau)
        v = max([similaridadeB, similaridadeM], key=abs)
        if v == 0:
            general[original]['neutro'].append(v)
        elif v == similaridadeB:
            general[original]['bom'].append(v)
        else: 
            general[original]['mau'].append(v)
    


def analyseSents(file):
    content = open(file, 'r').read()
    blocks = tolistString(content)
    for x in blocks: 
        general[x] = {'bom': [], 'mau': [], 'neutro': [], 'total': '', 'valor': 0.0}
        x_lem = lemmatization(x)
        x1 = catch_expressions(x, x_lem)
        x2 = catch_mult(x, x1)
        x_WS = remove_mystopwords(x2)
        x3 = catch_words(x, x_WS)
        #similarityWords(x, x3)
    return blocks
  

def viewComparacao():
    comp = input("Pretende efetuar a comparação de resultados?\n 0 - Não; 1 - Sim\n ")
    if comp == '1':
        ficheiroComp = input("Introduza o nome do ficheiro de comparação:  \n")
        dataframe1 = pd.read_csv(ficheiroComp, delimiter='|') 
        dataframe1.to_csv('comparacao.csv', index = None, header=['frase', 'sentimento'])
        df_words = pd.read_csv('comparacao.csv')
        frase = df_words['frase']
        sentimento = df_words['sentimento']
        for i in range(len(df_words)):
            if frase[i] in general:
                if (sentimento[i] ==general[frase[i]]['total'] ):
                    print("\n 📝 Frase:\n\"", frase[i], "\"\n ➡️ Esperado: "+ sentimento[i]  + "\t↪️ Obtido: " + general[frase[i]]['total'] + " ✅" )
                else:
                    print("\n 📝 Frase:\n\"", frase[i], "\"\n ➡️ Esperado: "+ sentimento[i]  + "\t↪️ Obtido: " + general[frase[i]]['total'] + " ❌")
        


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def writeToJSON():
    with open("output.json", "w") as outfile:
        json.dump(general, outfile, cls=NpEncoder)




blocksFile = analyseSents(sys.argv[1]) 

process_Sentiment()

viewComparacao()

writeToJSON()
