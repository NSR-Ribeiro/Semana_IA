# Escolha qualquer dataset no Kaagle

# Faça você mesmo! Faça como eu fiz!

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Faltas nas consultas médicas")

url = "https://raw.githubusercontent.com/NSR-Ribeiro/meus_datasets/refs/heads/main/cardio_train.csv"
df = pd.read_csv(url,delimiter=';')

st.dataframe(df)