import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import mysql.connector

LOGGER = get_logger(__name__)

def mysql_connection():
  mysql_config = st.secrets["mysql"]
  conn = mysql.connector.connect(
    host=mysql_config['host'],
    port=mysql_config['port'],
    database=mysql_config['database'],
    user=mysql_config['username'],
    password=mysql_config['password']
  )    
  return conn

def execute_query(query):
  conn = mysql_connection()
  cursor = conn.cursor()
  cursor.execute(query)

  # Obter nomes das colunas
  column_names = [col[0] for col in cursor.description]
  
  # Obter resultados
  result = cursor.fetchall()
  
  cursor.close()
  return result, column_names


def dataframe_query(query):
  resultado, nomeColunas = execute_query(query)
  dataframe = pd.DataFrame(resultado, columns=nomeColunas)
  return dataframe


########### Permissions #############

@st.cache_data
def GET_USERNAME(email):
  emailStr = f"'{email}'"
  return dataframe_query(f'''
  SELECT 
	  au.FULL_NAME AS 'Nome'
  FROM
  	ADMIN_USERS au 
  WHERE au.LOGIN = {emailStr}
  ''')

############ get lojas ############

@st.cache_data
def GET_LOJAS():
  return dataframe_query(f'''
  SELECT 
    te.ID AS 'ID Loja',
	  te.NOME_FANTASIA AS 'Loja'
  FROM
	  T_EMPRESAS te 
  WHERE te.ID NOT IN (100, 101, 102, 106, 107, 108, 109, 111, 113, 119, 120, 121, 123, 124, 125, 126, 127, 129, 130, 133, 134, 135, 138, 141, 142, 143, 144, 145, 146, 147, 155, 157, 158, 159, 161, 162, 163)
  ORDER BY te.NOME_FANTASIA
    ''')

  

# @st.cache_data
# def GET_INSUMOS_BLUE_ME_COM_PEDIDO():
#   return dataframe_query(f'''
# SELECT
#     vbmcp.tdr_ID AS tdr_ID,
#     vbmcp.ID_Loja AS ID_Loja,
#     vbmcp.Loja AS Loja,
#     vbmcp.Fornecedor AS Fornecedor,
#     vbmcp.Doc_Serie AS Doc_Serie,
#     vbmcp.Data_Emissao AS Data_Emissao,
#     vbmcp.Observacao AS Observacao,
#     vbmcp.Valor_Liquido AS Valor_Liquido,
#     vbmcp.Valor_Insumos AS Valor_Insumos,
#     CAST(DATE_FORMAT(CAST(vbmcp.Data_Emissao AS DATE), '%Y-%m-01') AS DATE) AS Primeiro_Dia_Mes,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Alimentos / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Alimentos,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Bebidas / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Bebidas,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Descartaveis_Higiene_Limpeza / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Descart_Hig_Limp,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Outros / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Outros,
#     virapc.Valor_Alimentos AS Valor_Alimentos,
#     virapc.Valor_Bebidas AS Valor_Bebidas,
#     virapc.Valor_Descartaveis_Higiene_Limpeza AS Valor_Descartaveis_Higiene_Limpeza,
#     virapc.Valor_Outros AS Valor_Outros
# FROM
#     View_BlueMe_Com_Pedido vbmcp
# 	LEFT JOIN View_Insumos_Receb_Agrup_Por_Categ virapc ON vbmcp.tdr_ID = virapc.tdr_ID
# ORDER BY Data_Emissao DESC;
# ''')

# @st.cache_data
# def GET_INSUMOS_BLUE_ME_COM_PEDIDO():
#   return dataframe_query(f'''
# SELECT
#     DISTINCT vbmcp.tdr_ID AS tdr_ID,
#     vbmcp.ID_Loja AS ID_Loja,
#     vbmcp.Loja AS Loja,
#     vbmcp.Fornecedor AS Fornecedor,
#     vbmcp.Doc_Serie AS Doc_Serie,
#     vbmcp.Data_Emissao AS Data_Emissao,
#     vbmcp.Observacao AS Observacao,
#     vbmcp.Valor_Liquido AS Valor_Liquido,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Alimentos / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Alimentos,
#     ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Bebidas / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Bebidas,
#     tps.DATA AS Data_Recebida
# FROM
#     View_BlueMe_Com_Pedido vbmcp
# 	LEFT JOIN View_Insumos_Receb_Agrup_Por_Categ virapc ON vbmcp.tdr_ID = virapc.tdr_ID
# 	LEFT JOIN T_DESPESA_RAPIDA tdr ON vbmcp.tdr_ID = tdr.ID
#     LEFT JOIN T_PEDIDOS tp ON tdr.FK_PEDIDO = tp.ID
#     LEFT JOIN T_PEDIDO_STATUS tps ON tp.ID = tps.FK_PEDIDO
# WHERE vbmcp.Observacao NOT IN ('HIGIENE E LIMPEZA', 'UTENSILIOS ') 
# ORDER BY Data_Emissao DESC;
# ''')



@st.cache_data
def GET_INSUMOS_BLUE_ME_COM_PEDIDO():
  return dataframe_query(f'''
SELECT
    vbmcp.tdr_ID AS tdr_ID,
    vbmcp.ID_Loja AS ID_Loja,
    vbmcp.Loja AS Loja,
    vbmcp.Fornecedor AS Fornecedor,
    vbmcp.Doc_Serie AS Doc_Serie,
    vbmcp.Data_Emissao AS Data_Emissao,
    vbmcp.Observacao AS Observacao,
    vbmcp.Valor_Liquido AS Valor_Liquido,
    ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Alimentos / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Alimentos,
    ROUND((vbmcp.Valor_Liquido * (virapc.Valor_Bebidas / virapc.Valor_Total_Insumos)), 2) AS Valor_Liq_Bebidas,
    MAX(tps.DATA) AS Data_Recebida  -- Seleciona a data mais recente para cada tdr_ID
FROM
    View_BlueMe_Com_Pedido vbmcp
    LEFT JOIN View_Insumos_Receb_Agrup_Por_Categ virapc ON vbmcp.tdr_ID = virapc.tdr_ID
    LEFT JOIN T_DESPESA_RAPIDA tdr ON vbmcp.tdr_ID = tdr.ID
    LEFT JOIN T_PEDIDOS tp ON tdr.FK_PEDIDO = tp.ID
    LEFT JOIN T_PEDIDO_STATUS tps ON tp.ID = tps.FK_PEDIDO
WHERE
    vbmcp.Observacao NOT IN ('HIGIENE E LIMPEZA', 'UTENSILIOS')
GROUP BY
    vbmcp.tdr_ID, vbmcp.ID_Loja, vbmcp.Loja, vbmcp.Fornecedor, vbmcp.Doc_Serie,
    vbmcp.Data_Emissao, vbmcp.Observacao, vbmcp.Valor_Liquido, virapc.Valor_Alimentos, virapc.Valor_Bebidas
ORDER BY
    Data_Emissao DESC;
''')

@st.cache_data
def GET_INSUMOS_BLUE_ME_SEM_PEDIDO():
  return dataframe_query(f'''  
  SELECT
      tdr_ID,
      Loja,
      Fornecedor,
      Class_Cont_Grupo_2,
      Doc_Serie,
      Data_Emissao,
      Data_Vencimento,
      Observacao,
      Valor_Liquido,
      Status
  FROM (
    SELECT
      tdr.ID AS tdr_ID,
      te.NOME_FANTASIA AS Loja,
      tf.CORPORATE_NAME AS Fornecedor,
      tdr.NF AS Doc_Serie,
      tdr.COMPETENCIA AS Data_Emissao,
      tdr.VENCIMENTO AS Data_Vencimento,
      tccg2.DESCRICAO AS Class_Cont_Grupo_2,
      tdr.OBSERVACAO AS Observacao,
      tdr.VALOR_LIQUIDO AS Valor_Liquido,
      tsp2.DESCRICAO AS Status,
      ROW_NUMBER() OVER (PARTITION BY tdr.ID
      ORDER BY
        tds.ID DESC) AS row_num
    FROM
      T_DESPESA_RAPIDA tdr
    JOIN T_EMPRESAS te ON tdr.FK_LOJA = te.ID
    LEFT JOIN T_FORNECEDOR tf ON tdr.FK_FORNECEDOR = tf.ID
    LEFT JOIN T_CLASSIFICACAO_CONTABIL_GRUPO_2 tccg2 ON tdr.FK_CLASSIFICACAO_CONTABIL_GRUPO_2 = tccg2.ID
    LEFT JOIN T_STATUS_PAGAMENTO tsp ON tdr.FK_STATUS_PGTO = tsp.ID
    LEFT JOIN T_CALENDARIO tc ON tdr.PREVISAO_PAGAMENTO = tc.ID
    LEFT JOIN T_CALENDARIO tc2 ON tdr.FK_DATA_REALIZACAO_PGTO = tc2.ID
    LEFT JOIN T_DESPESA_RAPIDA_ITEM tdri ON tdr.ID = tdri.FK_DESPESA_RAPIDA
    JOIN T_DESPESA_STATUS tds ON tdr.ID = tds.FK_DESPESA_RAPIDA
    JOIN T_STATUS ts ON tds.FK_STATUS_NAME = ts.ID
    JOIN T_STATUS_PAGAMENTO tsp2 ON ts.FK_STATUS_PAGAMENTO = tsp2.ID
    WHERE
      tdri.ID IS NULL
      AND tdr.FK_DESPESA_TEKNISA IS NULL
      AND tccg2.ID IN (437, 438) 
    ORDER BY DATE(tdr.COMPETENCIA) DESC
    ) AS subquery
    WHERE row_num = 1;
  ''')




def insert_into_compras_estoque(tdr_id, valor_alimentos, valor_bebidas):
  conn = mysql_connection()
  cursor = conn.cursor()

  query = """
  INSERT INTO T_RECEBIMENTO_APOS_CONTAGEM (FK_DESPESA, VALOR_ALIMENTOS, VALOR_BEBIDAS)
  VALUES (%s, %s, %s)
  """
  
  values = (tdr_id, valor_alimentos, valor_bebidas)

  try:
    cursor.execute(query, values)
    conn.commit()  # Confirma a transação
    st.success('Inserção realizada com sucesso!')
  except mysql.connector.Error as err:
    st.error(f'Erro: {err}')
  finally:
    cursor.close()
    conn.close()





