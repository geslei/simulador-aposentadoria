import streamlit as st
from datetime import date
from datetime import datetime
from math import floor

st.set_page_config(
    page_title='Simulador Previdencia - Servidores de Rondônia',
    layout='wide')

st.write(f"Isto é apenas uma simulação. A concessão depende da análise do órgão previdenciário. Essa simulação não substitui a consulta de um profissional especializado")
st.write(f"SITE EM DESENVOLVIMENTO")

st.header("Simulador de Aposentadoria Servidores de Rondônia - RPPS/IPERON")

# ENTRADAS DO USUÁRIO
col_1, col_2, col_3, col_4 = st.columns([0.5,0.5,0.5,0.5])
with col_1:
    data_nascimento = st.date_input("Insira sua Data de Nascimento", format="DD/MM/YYYY")
with col_2:  
    data_ingresso = st.date_input("Insira a data de ingresso no serviço público", format="DD/MM/YYYY")
with col_3: 
    tempo_contribuicao = st.number_input("Quantos anos de contribuição você possui?")
with col_4:    
    tempo_cargo = st.number_input("Há quantos anos está no cargo atual")

# calculando idade e salvando variável
idade = date.today().year - data_nascimento.year
# Se o aniversário ainda não ocorreu este ano, subtraia 1
if (date.today().month, date.today().day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1
# Arredonde para baixo
idade = floor(idade)

# calculando tempo de serviço e salvando variável
tempo_servico_publico = date.today().year - data_ingresso.year
if (date.today().month, date.today().day) < (data_ingresso.month, data_ingresso.day):
    tempo_servico_publico -= 1
# Arredonde para baixo
tempo_servico_publico = floor(tempo_servico_publico)

ano_atual = date.today().year
data_atual = datetime.now()

col_a, col_b, col_c, col_d = st.columns([1,1,1,1])   
with col_a:
    st.write(f"Você tem: {idade} anos")
with col_b:
    st.write(f"Você tem: {tempo_servico_publico} anos de serviço público")


# Caixa de seleção para o gênero
col1, col2, col3 = st.columns([1,1, 1])
with col1:
    genero = genero = st.selectbox("Qual é o seu gênero?", ['homem', 'mulher'])
with col2: 
    professor = st.selectbox("Você é professor (ensino infantil, fundamental ou médio)?", (['não', 'sim']))
with col3: 
    policial = st.selectbox("Você exerce atividade policial ou equiparada?", (['não', 'sim']))



#FUNÇÕES

#APOSENTADORIA POR IDADE
def verificar_aposentadoria_por_idade(idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, genero):
    if genero == "homem":
        if idade >= 65 and tempo_contribuicao >= 25 and tempo_servico_publico >= 10 and tempo_cargo >= 5:
            return f"Parabéns, você já pode se aposentar por IDADE!"
        else:
            anos_faltantes = max(0, 65 - idade, 25 - tempo_contribuicao, 10 - tempo_servico_publico, 5 - tempo_cargo)
            return f"Você ainda não pode se aposentar por IDADE. Faltam {anos_faltantes} anos."
    elif genero == "mulher":
        if idade >= 62 and tempo_contribuicao >= 25 and tempo_servico_publico >= 10 and tempo_cargo >= 5:
            return f"Parabéns, você já pode se aposentar por IDADE!"
        else:
            anos_faltantes = max(0, 62 - idade, 25 - tempo_contribuicao, 10 - tempo_servico_publico, 5 - tempo_cargo)
            return f"Você ainda não pode se aposentar por IDADE. Faltam {anos_faltantes} anos."


# APOSENTADORIA COMPULSÓRIA
def verificar_aposentadoria_compulsoria(idade):
    if idade >= 75:
        return f"Parabéns, você já pode se aposentar compulsoriamente!"
    else:
        anos_faltantes = max(0, 75 - idade)
        return f"Você ainda não pode se aposentar compulsoriamente. Faltam {anos_faltantes} anos."

#REGRA DE TRANSIÇÃO POR PONTOS
def verificar_aposentadoria_regra_transicao_pontos(genero, idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, ano_atual):
    if genero == "homem":
      while True:
          pontos = idade + tempo_contribuicao
          if ((idade >= 61 and ano_atual <= 2024) or (idade >= 62 and ano_atual >= 2024)) and \
            tempo_contribuicao >= 35 and tempo_servico_publico >= 20 and tempo_cargo >= 5 and \
            pontos >= 96 + min(max(0, ano_atual - 2021), 9):
              return f"Parabéns, você já pode se aposentar!" if ano_atual == datetime.now().year else f"Você poderá se aposentar pela regra de transição por pontos em {ano_atual}."
          idade += 1
          tempo_contribuicao += 1
          tempo_servico_publico += 1
          ano_atual += 1
    if genero == "mulher":
        while True:
            pontos = idade + tempo_contribuicao
            if ((idade >= 56 and ano_atual <= 2024) or (idade >= 57 and ano_atual >= 2024)) and \
              tempo_contribuicao >= 30 and tempo_servico_publico >= 20 and tempo_cargo >= 5 and \
              pontos >= 86 + min(max(0, ano_atual - 2021), 14):
                return f"Parabéns, você já pode se aposentar!" if ano_atual == datetime.now().year else f"Você poderá se aposentar pela regra de transição por pontos em {ano_atual}."
            idade += 1
            tempo_contribuicao += 1
            tempo_servico_publico += 1
            ano_atual += 1

# Regra de Transição por pedágio
def verificar_aposentadoria_regra_transicao_pedagio(genero, idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, data_atual):
    data_referencia = datetime(2021, 9, 14)
    anos_contribuicao_2021 = tempo_contribuicao - (data_atual.year - data_referencia.year)
    tempo_faltava = max(0, (35 if genero == 'homem' else 30) - anos_contribuicao_2021)

    while True:
        if genero == 'homem':
            if idade >= 60 and tempo_contribuicao >= 35 + tempo_faltava and tempo_servico_publico >= 20 and tempo_cargo >= 5:
                return f"Parabéns, você já pode se aposentar!" if data_atual.year == datetime.now().year else f"Você poderá se aposentar pela regra de transição por pedágio em {data_atual.year}."
        elif genero == 'mulher':
            if idade >= 57 and tempo_contribuicao >= 30 + tempo_faltava and tempo_servico_publico >= 20 and tempo_cargo >= 5:
                return f"Parabéns, você já pode se aposentar!" if data_atual.year == datetime.now().year else f"Você poderá se aposentar pela regra de transição por pedágio em {data_atual.year}."
        idade += 1
        tempo_contribuicao += 1
        data_atual = datetime(data_atual.year + 1, data_atual.month, data_atual.day)

    return f"Você poderá se aposentar em {data_atual.year}, faltam {data_atual.year - datetime.now().year} anos."

resultado_aposentadoria_por_idade = verificar_aposentadoria_por_idade(idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, genero)
st.write(resultado_aposentadoria_por_idade)

resultado_aposentadoria_compulsoria = verificar_aposentadoria_compulsoria(idade)
st.write(resultado_aposentadoria_compulsoria)

resultado_aposentadoria_regra_transicao_pontos = verificar_aposentadoria_regra_transicao_pontos(genero, idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, ano_atual)
st.write(resultado_aposentadoria_regra_transicao_pontos)

resultado_aposentadoria_regra_transicao_pedagio = verificar_aposentadoria_regra_transicao_pedagio(genero, idade, tempo_contribuicao, tempo_servico_publico, tempo_cargo, data_atual)
st.write(resultado_aposentadoria_regra_transicao_pedagio)
