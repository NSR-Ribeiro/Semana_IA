import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Dashboard de vendas:shopping_trolley:")

url = "https://labdados.com/produtos"
response = requests.get(url)
df= pd.DataFrame.from_dict(response.json())
# Valor total
st.metric('Receita',df['Preço'].sum())
# a qunatidade de vendas
st.metric('Qtde Vendas',df.shape[0])
# a quantidade de variáveis
st.metric('Qtde de variáveis',df.shape[1])
st.dataframe(df)
st.snow()

