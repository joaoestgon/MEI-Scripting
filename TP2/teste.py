'''from cmath import exp
from netrc import NetrcParseError
import requests
import pandas
from bs4 import BeautifulSoup
import numpy as np
import re
import matplotlib.pyplot as plt
import sys

import pandas as pd

dataframe1 = pd.read_csv("SentiLex.txt", delimiter=';') 
dataframe1.to_csv('SentiLex.csv', 
                  index = None, header=['word', 'n', 'sent'])
r = pd.read_csv("SentiLex.csv")

print(len(r['word']))'''


import nltk
from gensim.models import KeyedVectors
import gensim
import numpy as np
import spacy
load_model = spacy.load("pt_core_news_sm", disable = ['parser','ner'])
all_stopwords =  nltk.corpus.stopwords.words("portuguese")
f = "ISto é uma frase sem muito conteúdo apenas para testar. ISto é outra frase"

def lemmatization(texto):
    doc = load_model(f)
    return(" ".join([token.lemma_ for token in doc]))

print(lemmatization(f))


#Remover as stop words dos textos
#É capaz de pegar num título/texto ou até palavra apenas e remover as stop words
def remove_mystopwords(text):
    #fazer a tokenização por frases, para ser mais fácil
    f = nltk.sent_tokenize(text)
    tokens_filtered = []
    for sent in f:
        tokens = sent.split(" ")
        tokens_filtered += [word for word in tokens if not word in all_stopwords]
    return (" ").join(tokens_filtered)

#print(remove_mystopwords(f))




#model = KeyedVectors.load("model_300_20_sg.wv")

#for i in range(len(f)):
    # print(f[i])
    #f[i] = nltk.word_tokenize(f[i])
    #del(f[i][-1])
    #vetorPalavras = [model[x] for x in f[i] if x in model]
