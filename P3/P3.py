import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def histogramasCategoricas(df,anio):
    fig, axs = plt.subplots(nrows=1 ,ncols=5 ,figsize = (17,5.5))
    axs = axs.flatten()
    cols = df.columns.values
    count = 0
    total = len(df)
    cols_info = {'tipo_inst_2':('Tipo de Institución',(0,0.27)),
                 'region_sede':('Region de la sede',(0,0.35)),
                 'nivel_carrera_2': (' Tipo de carrera',(0,0.5)),
                 'cine_f_13_area':('Área de la carrera',(0,0.25)),
                 'GEN_ALU':('Genero de alumno',(0,0.4))}

    for i,col in enumerate(cols_info):
        title, ylim = cols_info[col]
        w = 0.45
        ax = axs[i]
        acre = (df['acreditada_carr'] == 'ACREDITADA')
        ndf = df[col]
        si_acre = ndf[acre]
        no_acre = ndf[acre==False]
        ass = si_acre.value_counts()
        an = no_acre.value_counts()
        bs = np.sort(ass.index.values)
        bn = np.sort(an.index.values)
        x = np.arange(len(bn))
        ax.bar(x-0.23,an[bs]/total,width= w,color='red',alpha = 0.5,label = 'Carrera no acreditada')
        ax.bar(x+0.23,ass[bs]/total,width= w,color='blue',alpha = 0.5,label = 'Carrera acreditada')
        ax.set_title(title)
        ax.grid(axis = 'both' ,color='gray', linestyle='--', linewidth=0.6)
        ax.xaxis.set_ticks(x)

        ax.set_xlim((-0.5,x[-1]+0.5))
        ax.set_ylim(ylim)
        if col == 'cine_f_13_area':
            bn = ['Administración y Derecho','Agricultura y Veterinaria',
                  'Artes y Humanidades', 'Ciencias Sociales','Ciencias',
                  'Educación','Ingeniería','Salud y Bienestar',
                  'Servicios','TIC']
            ax.legend()
        #ax.xaxis.set_ticks(bn)
        ax.set_xticklabels(bn, rotation=90)
    plt.show(block=False)
    fig.tight_layout()
    #plt.savefig(f'{anio}_Cat.png', format="png")

def histogramasNumericas(df,anio):
    fig, axs = plt.subplots(nrows=1 ,ncols=5 ,figsize = (17,3.5))
    axs = axs.flatten()
    cols = df.columns.values
    total = len(df)
    dic_metricas = {}
    cols_info = {'dur_total_carr':('Duración de la carrera',0.45,(0.5,7.5),(0,0.3)),
                'valor_arancel': ('Valor del arancel',0.22,(0,6.5),(0,0.25)),
                'edad_alu':('Edad del alumno',0.45,(16.5,30.5),(0,0.1)),
                'acre_inst_anio':('Años de acreditación restantes',0.45,(-0.5,7.5),(0,0.25)),
                'anios_U':('Años cursados por el alummno',0.45,(-0.5,10.5),(0,0.3))}

    df['dur_total_carr'] = np.ceil(df['dur_total_carr'].values).astype(np.int32)
    arancel_bins = np.arange(100)*500000
    df['valor_arancel'] = np.digitize(df['valor_arancel'].values, arancel_bins, right=True)/2

    for i,col in enumerate(cols_info):
        title, w, xlim, ylim = cols_info[col]
        ax = axs[i]
        acre = (df['acreditada_carr'] == 'ACREDITADA')
        ndf = df[col]
        si_acre = ndf[acre]
        no_acre = ndf[acre==False]
        ass = si_acre.value_counts()
        an = no_acre.value_counts()
        bs = np.sort(ass.index.values)
        bn = np.sort(an.index.values)
        xoffset = [0.23,0.11,0.23,0.23,0.23]
        ax.bar(bn-xoffset[i],an[bn]/total,width= w,color='red',alpha = 0.5,label = 'Carrera no acreditada')
        ax.bar(bs+xoffset[i],ass[bs]/total,width= w,color='blue',alpha = 0.5,label = 'Carrera acreditada')
        ax.set_title(title)
        ax.grid(axis = 'both' ,color='gray', linestyle='--', linewidth=0.6)
        #ax.xaxis.set_ticks(bn)
        #ax.legend()
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        if col == 'anios_U':
            total_nuevos = len(df[df['anios_U']==0])
            dic_metricas['NAnuevos'] =  round(an[bn][0]/total_nuevos,2)
            dic_metricas['Anuevos'] =  round(ass[bs][0]/total_nuevos,2)
        if col == 'valor_arancel':
            dic_metricas['NAarancel_mean'] = round(no_acre.mean(),1)
            dic_metricas['Aarancel_mean'] =  round(si_acre.mean(),1)
            dic_metricas['NAarancel_std'] =  round(no_acre.std(),1)
            dic_metricas['Aarancel_std'] =  round(si_acre.std(),1)
    fig.suptitle(f'Año {anio}', fontsize=16)
    plt.show(block=False)
    fig.tight_layout()
    return dic_metricas
    #plt.savefig(f'{anio}_Num.png', format="png")


anios = [2011,2012,2013,2014,2015,2016,2017,2018]
PANA = []#promedio de arancel no acreditado
PASA = []#promedio de arancel no acreditado
DANA = []#desviacion estandar de arancel no acreditado
DASA = []#desviacion estandar de arancel acreditado
NNA = []#cantidad de alumnos nuevos no acreditado
NSA = []#cantidad de alumnos nuevos acreditado
a = []

for anio in anios:
    filename = f'data_acre/modif_acre_{anio}.csv'
    df = pd.read_csv(filename, error_bad_lines=False)
    dic = histogramasNumericas(df,anio)
    histogramasCategoricas(df,anio)

    PANA = np.append(PANA,dic['NAarancel_mean'])
    PASA = np.append(PASA,dic['Aarancel_mean'])
    DANA = np.append(DANA,dic['NAarancel_std'])
    DASA = np.append(DASA,dic['Aarancel_std'])
    NNA = np.append(NNA,dic['NAnuevos'])
    NSA = np.append(NSA,dic['Anuevos'])


'''
anio = 2011
filename = f'data_acre/modif_acre_{anio}.csv'
df = pd.read_csv(filename, error_bad_lines=False)
dic = histogramasNumericas(df,anio)
#imprime columnas
#cols = df.columns.values
#for i in range(len(cols)):
#    print(i+1,cols[i])

fig, ax = plt.subplots(figsize = (10,3))
a = df['edad_alu'].value_counts()
b = np.sort(a.index.values)
ax.bar(b,a[b],color='orange',alpha = 0.7)
plt.show(block=False)
fig.tight_layout()

cols_title = {'tipo_inst_2':'Tipo de Institución',
              'region_sede':'Region de la sede',
              'nivel_carrera_2': ' Tipo de carrera',
              'cine_f_13_area':'Área de la carrera',
              'GEN_ALU':'Genero de alumno',
              'dur_total_carr':'Duración de la carrera',
              'valor_arancel': 'Valor del arancel',
              'edad_alu':'Edad del alumno',
              'acre_inst_anio':'Años de acreditación restantes',
              'anios_U':'Años cursados por el alummno'}
'''
