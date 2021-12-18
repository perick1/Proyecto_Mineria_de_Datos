import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def pltMetrica(x, y1, y2, ylabel= '', title= ''):
    fig, ax = plt.subplots(figsize = (6,4))
    ax.plot(x,y1,'o-',color = 'red',alpha = 0.6,label = 'Carreras No Acreditadas')
    ax.plot(x,y2,'o-',color = 'blue',alpha = 0.6,label = 'Carreras Acreditadas')
    ax.grid(axis = 'both' ,color='gray', linestyle='--', linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel('Año')
    ax.set_ylabel(ylabel)
    ax.legend()
    plt.show(block=False)
    fig.tight_layout()

filename = 'valores_temporales.csv'
idx = ['mean_no_ac', 'mean_ac', 'std_no_ac', 'std_ac', 'nuevos_no_ac', 'nuevos_ac']
df = pd.read_csv(filename, error_bad_lines=False)
df.index = idx

x = df.columns.values
pltMetrica(x,df.iloc[4],df.iloc[5],ylabel= '',title= '% de alumnos nuevos (recien ingresados)')
pltMetrica(x,df.iloc[0],df.iloc[1],ylabel= 'Valor del arancel [millones $CLP]',title= 'Promedio del valor del arancel por año')

print(df)
