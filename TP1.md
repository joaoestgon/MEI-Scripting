# Stanza

Links Úteis:

https://stanfordnlp.github.io/stanza/

https://github.com/stanfordnlp/stanza

https://analyticsindiamag.com/stanza-a-new-nlp-library-by-stanford/

https://analyticsindiamag.com/how-to-use-stanza-by-stanford-nlp-group-with-python-code/

https://openbase.com/python/stanza/documentation



Instalação: pode ser feita via pip, conda ou github source code.


## O que é Stanza? 
* Santza é uma coleção de ferramentas efecientes e precisas utilizadas na análise linguística de linguagem humana.

* Desde texto em bruto até análise sintática e reconhecimento de entidades, Stanza tem modelos de PNL de última geração para um conjunto muito grande de linguagens.

* Por outras palavras converte tecto em listas de frases e palavras, fazendo o seu reconhecimento e gerando formas básicas dessas palavras, reconhecer características morfológicas, e sintáticas, tendo por base os formalismos de cerca de 70 línguas.

* Stanza é construído com base em redes neuronais, permitindo avaliação eficiente dos próprios dados anotados.

Os Stanzas são muito utilizados para organizar poesia. Nomeadamente para refletir sobre a intenção de um poeta, o humor e ritmo do poema, ou os vários temas e personagens em acção dentro do poema. 


## Como utilizar?
Para começar as anotações com Stanza, é necessário inicializar um Pipeline que contém o processador que permite satisfazer as tarefas que desejamos.
Isso é feito da seguinte forma:

``` 
import stanza 

stanza.download('en')       # Faz download dos modelos em Ingles para o pipeline
nlp = stanza.Pipeline('en', processors='tokenize,pos', use_gpu=True, pos_batch_size=3000) # Constrói o pipeline, com processo de tokenização, utilização de gpu e no máximo 3000 palavras
doc = nlp("Scripting is a cool subject") # Corre o pipeline com o texto dado
print(doc) 
```
