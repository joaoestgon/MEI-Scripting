
from bs4 import BeautifulSoup
import re
import requests

def treatInfo(url):
    final = []
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    #Retirar todas as headlines do site para analisar os sentimentos
    headlines = soup.find('body').find_all('h4', 'headline')
    #headlines = ['isto é um ponto forte muito lindo, vamos testar outro ponto forte', 'isto é outro ponto fraco', 'que deixa muito a desejar', 'que coisa muito linda']
    for x in headlines: 
        x = x.text.strip()
        final.append(x)
    return final
    

url='https://www.publico.pt/online'

print(treatInfo(url))
