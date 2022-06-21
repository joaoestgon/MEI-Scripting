import csv
import re
import time


def CleanRegEx() :
    with open('SentiLex.csv', "r", encoding='utf-8') as file:
        data = file.read().splitlines()
        for row in data :
            if (re.search("[\s]+", row)) :
                print(row)


def Read() :

    with open('SentiLex.csv', "r", encoding='utf-8') as file:
        data = file.read().splitlines()
        lista = []
        for row in data :
            if (re.search("[\s]+", row)) :
                lista.append(row)
        return (lista)

def Delete(lista) :

    with open('SentiLex.csv', "r", encoding='utf-8') as inp, open('first_edit.csv', 'w', encoding='utf-8') as out:
        writer = csv.writer(out)

        myText = open('ranfado.txt','w', encoding='utf-8')
        
        
        cnt = 0
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
                print('Escrever no ficheiro: ' + row)
                myText.write(row+'\n')

        myText.close()
                    

#print(Read())

Delete(Read())