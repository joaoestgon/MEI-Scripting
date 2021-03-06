# Stanza

## O que é Stanza? 

* Stanza é uma coleção de ferramentas Python utilizadas na análise linguística de linguagem humana.

* Desde texto em bruto até análise sintática e reconhecimento de entidades, Stanza tem modelos de PNL de última geração para diversas linguagens.

* Por outras palavras converte texto em listas de frases e palavras, fazendo o seu reconhecimento e gerando formas básicas dessas palavras, reconhecer características morfológicas, e sintáticas, tendo por base os formalismos de cerca de 70 línguas.

* Stanza é construído com base em redes neuronais, permitindo avaliação eficiente dos próprios dados anotados. Por consequência deste facto, é recomendável a utilização de máquinas orientadas para GPU, permitindo uma melhor performance do software.

* Módulos Stanza têm por base a biblioteca PyTorch.

Os Stanzas são muito utilizados para organizar poesia. Nomeadamente para refletir sobre a intenção de um poeta, o humor e ritmo do poema, ou os vários temas e personagens em acção dentro do poema. 

Investigadores na área esperam conseguir, através da Stanza, aplicações e pesquisas NLP multi linguísticas, que tragam novos conhecimentos acerca das mais diversas línguas humanas.

## Instalação

### pip

```pip install stanza```

### conda

```conda install -c stanfordnlp stanza```

### github source code

```
git clone https://github.com/stanfordnlp/stanza.git
cd stanza
pip install -e
```

## Limitações

* Os modelos Stanza disponíveis para download foram treinados num único dataset, pelo que a sua robustez deve ser verificada com dados de fontes alternativas.

* A biblioteca Stanza está otimizada para precisão dos resultados, podendo por vezes ser computacionalmente pouco eficiente.

* Outras técnicas de NLP devem ser utilizdas em conjunto com a Stanza, de modo a obter análises de textos mais completas.

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

Um pipeline também pode ser inicializado com um dicionário ou listas de documentos.

``` import stanza

config = {
        # Comma-separated list of processors to use
	'processors': 'tokenize,mwt,pos',
        # Language code for the language to build the Pipeline in
        'lang': 'fr',
        # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
        # You only need model paths if you have a specific model outside of stanza_resources
	'tokenize_model_path': './fr_gsd_models/fr_gsd_tokenizer.pt',
	'mwt_model_path': './fr_gsd_models/fr_gsd_mwt_expander.pt',
	'pos_model_path': './fr_gsd_models/fr_gsd_tagger.pt',
	'pos_pretrain_path': './fr_gsd_models/fr_gsd.pretrain.pt',
        # Use pretokenized text as input and disable tokenization
	'tokenize_pretokenized': True
}
nlp = stanza.Pipeline(**config) # Initialize the pipeline using a configuration dict
doc = nlp("Van Gogh grandit au sein d'une famille de l'ancienne bourgeoisie .") # Run the pipeline on the pretokenized input text
print(doc) # Look at the result 



import stanza
nlp = stanza.Pipeline(lang="en") # Initialize the default English pipeline
documents = ["This is a test document.", "I wrote another document for fun."] # Documents that we are going to process
in_docs = [stanza.Document([], text=d) for d in documents] # Wrap each document with a stanza.Document object
out_docs = nlp(in_docs) # Call the neural pipeline on this list of documents
print(out_docs[1]) # The output is also a list of stanza.Document objects, each output corresponding to an input Document object 
```



https://stanfordnlp.github.io/stanza/pipeline.html#pipeline


## Bibliografia

https://stanfordnlp.github.io/stanza/

https://github.com/stanfordnlp/stanza

https://analyticsindiamag.com/stanza-a-new-nlp-library-by-stanford/

https://analyticsindiamag.com/how-to-use-stanza-by-stanford-nlp-group-with-python-code/
