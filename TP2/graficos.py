import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import sys
general = {}

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

with open(sys.argv[1]) as d:
    general = json.load(d)

def desenharPlot():
    # Defining coordinates to be plotted on X and Y axes respectively
    x = []
    y = []
    i = 0
    for value in general:
        y.append(general[value]['valor'])
        x.append(i)
        i += 1
    """ Example 9 """
    # Plot continuous green line with circle markers

    fig, ax = plt.subplots()
    #ax.plot(y, 'go-')
    ax.plot(y, 'b*-')
    ax.plot(y, 'ro')
    # Plot axes labels and show the plot
    # set the x-spine
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    #ax.yaxis.tick_left()

    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    #ax.xaxis.tick_bottom()


    plt.ylabel('Sentimento')
    plt.xlabel('Posição da Notícia')
    plt.show()


desenharPlot()