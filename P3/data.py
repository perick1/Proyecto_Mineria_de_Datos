import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.relativedelta import *
from datetime import date
from sklearn.preprocessing import StandardScaler
import umap

'''
#################################################################
                        FUNCIONES
#################################################################
'''

def seleccionar_cols(filename ,anio ,cols):
    df = pd.read_csv(filename, error_bad_lines=False)
    df_filtered = df[cols]
    name = f'data_acre/data_acre_{anio}'
    df_filtered.to_csv(name+'.csv',index=False)
    return df_filtered

def modificar_cols(filename , anio):
    df = pd.read_csv(filename, error_bad_lines=False)
    #df = df.iloc[:20]
    ###############
    # numericas
    ###############
    #modificar genero
    df['GEN_ALU'] = df['GEN_ALU'].replace(to_replace = {1:'masculino' ,
                                                        2:'femenino'})
    #cambiar anios de acreditacion
    df['acre_inst_anio'] = df['acre_inst_anio'].fillna(0)

    #fecha de nacimiento
    df = df.dropna()
    df.index = np.arange(len(df))
    nac = pd.Series(data=np.arange(len(df)), index=np.arange(len(df)))
    ing = pd.Series(data=np.arange(len(df)), index=np.arange(len(df)))
    for i in range(len(df)):
        fecha_nac = str(int(df.iloc[i]['FEC_NAC_ALU']))
        fecha_ingreso = int(df.iloc[i]['anio_ing_carr_ori'])
        today = date(anio, 2, 1)
        nac.iloc[i] = int((today - date(int(fecha_nac[:4]), int(fecha_nac[4:]), 1)).days/365)
        ing.iloc[i] = int((today - date(fecha_ingreso, 1, 1)).days/365)
    df['edad_alu']  = nac
    df['anios_U']   = ing
    df = df.loc[df['edad_alu']>=0]
    df = df.loc[df['anios_U']>=0]
    df['dur_total_carr'] = df['dur_total_carr'] / 2

    cols_filter = ['tipo_inst_2','region_sede','nivel_carrera_2','cine_f_13_area','GEN_ALU',
                   'acreditada_carr','dur_total_carr','valor_arancel','edad_alu','acre_inst_anio','anios_U']


    name = f'data_acre/modif_acre_{anio}'
    df[cols_filter].to_csv(name+'.csv',index=False)

    #return df

def codificar_OH(df):
    dummy1 = pd.get_dummies(df.tipo_inst_2)
    dummy2 = pd.get_dummies(df.nivel_carrera_2)
    df_merged = pd.concat([df,dummy1],axis = 'columns')
    df_merged = pd.concat([df_merged,dummy2],axis = 'columns')

    return df_merged

def Umap_clusters(df):
    cols = ['dur_total_carr','valor_arancel','acre_inst_anio','anios_U','edad_alu']
    data = df[cols]
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    #return data
    fit = umap.UMAP()
    u = fit.fit_transform(data_scaled[:500])
    plt.scatter(u[:,0], u[:,1])
    plt.show(block=False)
'''
#################################################################
                        PRUEBAS
#################################################################
'''

cols = ['tipo_inst_2','nomb_inst','region_sede','nivel_carrera_2','cine_f_13_area',
        'acreditada_carr','cat_periodo','GEN_ALU','FEC_NAC_ALU','anio_ing_carr_ori',
        'dur_total_carr','valor_arancel','acre_inst_anio']

anios = [2011,2012,2013,2014,2015,2016,2017,2018]

for anio in anios:
    #filename = f'data/{anio}.csv'
    #seleccionar_cols(filename ,anio ,cols)
    filename = f'data_acre/data_acre_{anio}.csv'
    modificar_cols(filename , anio)

#filename = f'data_acre/data_acre_{anio}.csv'
#df = modificar_cols(filename , anio)

#filename = f'data_acre/modif_acre_{anio}.csv'
#df = pd.read_csv(filename, error_bad_lines=False)

#df_cod = codificar_OH(df)
#data = Umap_clusters(df_cod)
#df = pd.read_csv('data/2018.csv', error_bad_lines=False)
#df_fitered = df[cols]
#data_acre_2018
#df_fitered.to_csv(name+'.csv',index=False)
#df_num = df.select_dtypes(include=np.number)
#df_cat = df.drop(df_num.columns.values,axis = 'columns')
#df_cat.iloc[0]
#df.hist(column='FEC_NAC_ALU',bins = 1000)
#plt.show()

#anio = 2016
#filename =  f'data_acre/data_acre_{anio}.csv'
#df = pd.read_csv(filename, error_bad_lines=False)
#a = df.iloc[2]['acre_inst_desde_hasta']
#print(df.isna().sum())
