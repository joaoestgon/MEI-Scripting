
import requests
import pandas
from bs4 import BeautifulSoup
import numpy as np

df = pandas.read_csv('sentiment.csv')
sen = df['word']
cat = df['sentiment']

url='https://www.bbc.com/news'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
headlines = soup.find('body').find_all('h3')
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


