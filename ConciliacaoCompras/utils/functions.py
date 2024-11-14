import streamlit as st
import pandas as pd
from workalendar.america import Brazil
from datetime import datetime, timedelta
from utils.queries import *


def filtrar_por_datas(dataframe, data_inicio, data_fim, categoria):
  data_inicio = pd.Timestamp(data_inicio)
  data_fim = pd.Timestamp(data_fim)
 
  dataframe.loc[:, categoria] = pd.to_datetime(dataframe[categoria], errors='coerce')
  
  dataframe_filtered = dataframe.loc[
      (dataframe[categoria] >= data_inicio) & (dataframe[categoria] <= data_fim)
  ]
  
  return dataframe_filtered


def filtrar_por_classe_selecionada(dataframe, classe, valor_selecionado):
  if valor_selecionado:
    dataframe = dataframe[dataframe[classe] == valor_selecionado]
  return dataframe



  # Função para criar o novo DataFrame com base no tdr_ID informado
# def criar_novo_dataframe(insumos_com_pedido, insumos_sem_pedido, tdr_id):
#     # Verificar se o ID está no DataFrame insumos_com_pedido
#     if tdr_id in insumos_com_pedido['tdr_ID'].values:
#         tupla = insumos_com_pedido.loc[insumos_com_pedido['tdr_ID'] == tdr_id]
#         novo_df = pd.DataFrame({
#             'FK_TDR': [tupla['tdr_ID'].values[0]],
#             'VALOR_ALIMENTOS': [tupla['Valor_Liq_Alimentos'].values[0]],
#             'VALOR_BEBIDAS': [tupla['Valor_Liq_Bebidas'].values[0]]
#         })
#     # Caso o ID esteja no DataFrame insumos_sem_pedido
#     elif tdr_id in insumos_sem_pedido['tdr_ID'].values:
#         tupla = insumos_sem_pedido.loc[insumos_sem_pedido['tdr_ID'] == tdr_id]
#         if tupla['Class_Cont_Grupo_2'].values[0] == 'ALIMENTOS':
#             novo_df = pd.DataFrame({
#                 'FK_TDR': [tupla['tdr_ID'].values[0]],
#                 'VALOR_ALIMENTOS': [tupla['Valor_Liquido'].values[0]],
#                 'VALOR_BEBIDAS': [0]  # Colocamos zero para indicar ausência de valor
#             })
#         elif tupla['Class_Cont_Grupo_2'].values[0] == 'BEBIDAS':
#             novo_df = pd.DataFrame({
#                 'FK_TDR': [tupla['tdr_ID'].values[0]],
#                 'VALOR_ALIMENTOS': [0],  # Colocamos zero para indicar ausência de valor
#                 'VALOR_BEBIDAS': [tupla['Valor_Liquido'].values[0]]
#             })
#     else:
#         novo_df = pd.DataFrame(columns=['FK_TDR', 'VALOR_ALIMENTOS', 'VALOR_BEBIDAS'])  # Caso o ID não seja encontrado

#     return novo_df

