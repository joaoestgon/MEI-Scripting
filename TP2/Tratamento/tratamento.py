import csv
import re
import pandas as pd

def LerParaLista() :

    with open('SentiLex.csv', "r", encoding='utf-8') as file:
        data = file.read().splitlines()
        lista = []
        for row in data :
            if (re.search("[\s]+", row)) :
                lista.append(row)
        return (lista)

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
    
            row = str(row)
            row = re.sub(r'\[|\]', '', row)
            row = re.sub(r'\'', '', row)
            row = re.sub(r', ', ',', row)

            flag = 0

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
