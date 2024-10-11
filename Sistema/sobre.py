import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('consultas.db')
c = conn.cursor()

# Criar tabela se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL
    )
''')
conn.commit()

# Função para exibir consultas
def mostrar_consultas():
    c.execute('SELECT * FROM consultas')
    return c.fetchall()

# Função para agendar consulta
def agendar_consulta(nome, data, hora):
    c.execute('INSERT INTO consultas (nome, data, hora) VALUES (?, ?, ?)', (nome, data, hora))
    conn.commit()

# Função para cancelar consulta
def cancelar_consulta(consulta_id):
    c.execute('DELETE FROM consultas WHERE id = ?', (consulta_id,))
    conn.commit()

# Título da aplicação
st.title("Sistema de Marcação de Saúde")

# Seção para agendar consulta
st.header("Agendar Consulta")
nome = st.text_input("Nome do Paciente")
data = st.date_input("Data da Consulta")
hora = st.time_input("Hora da Consulta")

if st.button("Agendar"):
    if nome and data and hora:
        agendar_consulta(nome, str(data), str(hora))
        st.success("Consulta agendada com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos.")

# Seção para visualizar consultas
st.header("Consultas Agendadas")
consultas = mostrar_consultas()
if consultas:
    df = pd.DataFrame(consultas, columns=["ID", "Nome", "Data", "Hora"])
    st.write(df)

    # Seção para cancelar consulta
    st.header("Cancelar Consulta")
    consulta_id = st.number_input("ID da Consulta a Cancelar", min_value=1)
    if st.button("Cancelar"):
        cancelar_consulta(consulta_id)
        st.success("Consulta cancelada com sucesso!")
else:
    st.write("Nenhuma consulta agendada.")

# Fechar a conexão ao banco de dados ao final
conn.close()
