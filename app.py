import streamlit as st
from datetime import date
from math import floor

st.set_page_config(
    page_title='Simulador Previdencia - Servidores de Rondônia',
    layout='wide')

st.header("Simulador de Aposentadoria Servidores de Rondônia - RPPS/IPERON")

col_1, col_2 = st.columns([1,1])
with col_1:
    data_nascimento = st.date_input("Insira sua Data de Nascimento", format="DD/MM/YYYY")
with col_2:  
    data_ingresso = st.date_input("Insira a data de ingresso no serviço público", format="DD/MM/YYYY")


idade = date.today().year - data_nascimento.year

# Se o aniversário ainda não ocorreu este ano, subtraia 1
if (date.today().month, date.today().day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1
# Arredonde para baixo
idade = floor(idade)
st.write(f"Você tem: {idade} anos")
st.write(f"Atenção!!! Isto é apenas uma simulação e a concessão depende da análise do órgão previdenciário. Essa simulação é apenas um referencial e não substitui a consulta de um profissional especializado"")
