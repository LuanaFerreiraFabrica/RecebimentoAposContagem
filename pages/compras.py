import streamlit as st
import pandas as pd
from datetime import datetime
from utils.queries import *
from utils.functions import *

st.set_page_config(
  layout='wide',
  page_title='Compras',
  page_icon=':ballot_box_with_ballot:',
  initial_sidebar_state="collapsed"
)

if 'loggedIn' not in st.session_state or not st.session_state['loggedIn']:
  st.switch_page('main.py')


def limpar_sessao(session):
  dados_login = session.get('loggedIn', {})
  session.clear()
  session['loggedIn'] = dados_login


def reset_quantidades(df):
  df['Quantidade'] = 0.0
  return df


st.title("Compras que chegaram após a Contagem de Estoque") 

# Obter as lojas e insumos
df_lojas = GET_LOJAS()
lojas = df_lojas['Loja'].tolist()
loja_ids = dict(zip(df_lojas['Loja'], df_lojas['ID Loja']))
         

insumos_com_pedido = GET_INSUMOS_BLUE_ME_COM_PEDIDO()
insumos_sem_pedido = GET_INSUMOS_BLUE_ME_SEM_PEDIDO()
insumos_sem_pedido['Data_Emissao'] = pd.to_datetime(insumos_sem_pedido['Data_Emissao'], errors='coerce')
insumos_com_pedido['Data_Emissao'] = pd.to_datetime(insumos_com_pedido['Data_Emissao'], errors='coerce')

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
  lojas_selecionadas = st.selectbox(label='Loja:', options=lojas, key='lojas_multiselect')
with col2:
  data_inicio = st.date_input('Inicio:', value=datetime.today()-timedelta(days=30), key='data_inicio_input', format="DD/MM/YYYY")
with col3:
  data_fim = st.date_input('Fim:', value=datetime.today(), key='data_fim_input', format="DD/MM/YYYY")



insumos_com_pedido = filtrar_por_datas(insumos_com_pedido, data_inicio, data_fim, 'Data_Emissao')
insumos_sem_pedido = filtrar_por_datas(insumos_sem_pedido, data_inicio, data_fim, 'Data_Emissao')
insumos_com_pedido = filtrar_por_classe_selecionada(insumos_com_pedido, 'Loja', lojas_selecionadas)
insumos_sem_pedido = filtrar_por_classe_selecionada(insumos_sem_pedido, 'Loja', lojas_selecionadas)

insumos_sem_pedido['Data_Emissao'] = insumos_sem_pedido['Data_Emissao'].dt.strftime('%d-%m-%Y')
insumos_com_pedido['Data_Emissao'] = insumos_com_pedido['Data_Emissao'].dt.strftime('%d-%m-%Y')
insumos_com_pedido['Data_Recebida'] = insumos_com_pedido['Data_Recebida'].dt.strftime('%d-%m-%Y %H:%M:%S')


with st.container(border=True):
  st.subheader('Insumos com Pedido')
  st.dataframe(insumos_com_pedido, use_container_width=True, hide_index=True)

with st.container(border=True):
  st.subheader('Insumos sem Pedido')  
  st.dataframe(insumos_sem_pedido, use_container_width=True, hide_index=True)


# Input para o tdr_ID
tdr_id_input = st.text_input('Digite o tdr_ID:')


def criar_novo_dataframe(insumos_com_pedido, insumos_sem_pedido, tdr_id_input):
    # Verificar se o usuário digitou algo
    if tdr_id_input:
        # Converter o input para int, se necessário
        try:
            tdr_id_input = int(tdr_id_input)
        except ValueError:
            st.error("Por favor, insira um número válido para o tdr_ID.")
            tdr_id_input = None

        # Procurar nas tabelas pelo tdr_ID
        if tdr_id_input is not None:
            # Filtrar as tabelas para o tdr_ID especificado
            resultado_com_pedido = insumos_com_pedido[insumos_com_pedido['tdr_ID'] == tdr_id_input]
            resultado_sem_pedido = insumos_sem_pedido[insumos_sem_pedido['tdr_ID'] == tdr_id_input]
            
            # Exibir o resultado com pedido, se encontrado
            if not resultado_com_pedido.empty:
                st.write("Resultado encontrado em Insumos Com Pedido:")
                st.write(resultado_com_pedido)
                tupla = insumos_com_pedido.loc[insumos_com_pedido['tdr_ID'] == tdr_id_input]
                novo_df = pd.DataFrame({
                    'FK_TDR': [tupla['tdr_ID'].values[0]],
                    'VALOR_ALIMENTOS': [tupla['Valor_Liq_Alimentos'].values[0]],
                    'VALOR_BEBIDAS': [tupla['Valor_Liq_Bebidas'].values[0]]
                })
            
            # Verificar e exibir o resultado sem pedido
            elif not resultado_sem_pedido.empty:
                st.write("Resultado encontrado em Insumos Sem Pedido:")
                st.write(resultado_sem_pedido)
                tupla = insumos_sem_pedido.loc[insumos_sem_pedido['tdr_ID'] == tdr_id_input]
                
                
                # Verificar se a Class_Cont_Grupo_2 é "ALIMENTOS" ou "BEBIDAS"
                class_grupo = resultado_sem_pedido['Class_Cont_Grupo_2'].iloc[0]
                if class_grupo == "ALIMENTOS":
                    st.write("Este item pertence à categoria: ALIMENTOS")
                    novo_df = pd.DataFrame({
                        'FK_TDR': [tupla['tdr_ID'].values[0]],
                        'VALOR_ALIMENTOS': [tupla['Valor_Liquido'].values[0]],
                        'VALOR_BEBIDAS': [0]  # Colocamos zero para indicar ausência de valor
                    })
                elif class_grupo == "BEBIDAS":
                    st.write("Este item pertence à categoria: BEBIDAS")
                    novo_df = pd.DataFrame({
                        'FK_TDR': [tupla['tdr_ID'].values[0]],
                        'VALOR_ALIMENTOS': [0],  # Colocamos zero para indicar ausência de valor
                        'VALOR_BEBIDAS': [tupla['Valor_Liquido'].values[0]]
                    })
                else:
                    st.write("Este item não pertence às categorias ALIMENTOS ou BEBIDAS.")
                    return
            
            else:
                st.write("Nenhum resultado encontrado para o tdr_ID informado.")
                return


            st.write(novo_df)

            if st.button("Inserir no banco"):
                if novo_df is not None:
                    # Extrai os valores da tupla no novo DataFrame
                    tdr_id = int(novo_df["FK_TDR"].iloc[0])
                    valor_alimentos = float(novo_df["VALOR_ALIMENTOS"].iloc[0])
                    valor_bebidas = float(novo_df["VALOR_BEBIDAS"].iloc[0])

                    # Chama a função de inserção
                    insert_into_compras_estoque(tdr_id, valor_alimentos, valor_bebidas)
                    st.success(f'Registro {tdr_id} inserido')
                else:
                    st.warning("Nenhum dado para inserir no banco de dados.")
                
    return
    


criar_novo_dataframe(insumos_com_pedido, insumos_sem_pedido, tdr_id_input)






# # Botão para registrar a contagem
# if st.button("Registrar Contagem", key="registrar"):
#   # Filtrar o DataFrame para incluir apenas as quantidades diferentes de 0
#   df_filtrado = df_editado[(df_editado['Quantidade'] != 0) & (df_editado['Quantidade'].notna())]
#   id_loja_selecionada = loja_ids[lojas_selecionadas]

#   # Armazenar os dados no estado da sessão para confirmação
#   st.session_state['confirmar_contagem'] = True
#   st.session_state['df_filtrado'] = df_filtrado
#   st.session_state['id_loja_selecionada'] = id_loja_selecionada
#   # st.session_state['data_contagem'] = data_contagem.strftime("%d-%m-%Y")
#   st.session_state['data_contagem_banco'] = datetime_banco
#   st.session_state['data_contagem_formatado'] = datetime_formatado

# # Verificar se o estado de confirmação está ativo
# if 'confirmar_contagem' in st.session_state and st.session_state['confirmar_contagem']:
#   st.subheader('Tem certeza? Confirme as informações:')
#   st.write("Loja selecionada:", lojas_selecionadas)
#   st.write("Data e hora selecionadas:", st.session_state['data_contagem_formatado'])
#   st.dataframe(st.session_state['df_filtrado'])

#   # Botão para confirmar e inserir no banco de dados
#   if st.button("Confirmar", key="confirmar"):
#     # Inserir os dados no banco
#     for _, row in st.session_state['df_filtrado'].iterrows():
#       fk_insumo = row['ID Insumo']
#       quantidade_insumo = row['Quantidade']
#       insert_into_contagem_insumos(st.session_state['id_loja_selecionada'], fk_insumo, quantidade_insumo, st.session_state['data_contagem_banco'])

#     st.success("Contagens registradas com sucesso!")
#     st.session_state['df_insumos'] = reset_quantidades(df_editado)
#     limpar_sessao(st.session_state)

#     # Rerun para atualizar a página
#     st.rerun()
