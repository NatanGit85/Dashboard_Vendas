import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

@st.cache_data
def converter_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def mensagem_sucesso(): 
    sucesso=st.success("Arquivo baixado com sucesso!")
    time.sleep(3)
    sucesso.empty()

st.title("DADOS BRUTOS")
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')
#st.dataframe(dados)
with st.expander("Colunas"):
    colunas=st.multiselect("Selecione as colunas:",list(dados.columns),list(dados.columns))
st.sidebar.title("Filtros")

with st.sidebar.expander("Nome do produto:"):
    produto=st.multiselect("Selecione os produtos:",dados["Produto"].unique(),dados["Produto"].unique())
    
with st.sidebar.expander("Categoria do produto:"):
    categorias=st.multiselect("Selecione as categorias:",dados["Categoria do Produto"].unique(),dados["Categoria do Produto"].unique())

with st.sidebar.expander("Preço do produto"):
    preco=st.slider("Selecione o preço:",0,5000,(0,5000))

with st.sidebar.expander("Frete da venda"):
    frete=st.slider("Selecione o frete:",0,250,(0,250))    
    
with st.sidebar.expander("Data da compra"):
    data_compra=st.date_input("Selecione a data:",(dados["Data da Compra"].min(),dados["Data da Compra"].max()))
    
with st.sidebar.expander("Vendedor"):
    vendedor=st.multiselect("Selecione os vendedores:",dados["Vendedor"].unique(),dados["Vendedor"].unique())
    
with st.sidebar.expander("Local da compra"):
    local_compra=st.multiselect("Selecione os Locais de compra:",dados["Local da compra"].unique(),dados["Local da compra"].unique())

with st.sidebar.expander("Selecione a nota de avaliação da compra:"):
    avaliacao=st.slider("Selecione a avaliação:",0,5,(0,5))
    

with st.sidebar.expander("Selecione o tipo de pagamento:"):
    pagamento=st.multiselect("Selecione o tipo de pagamento:",dados["Tipo de pagamento"].unique(),dados["Tipo de pagamento"].unique())

with st.sidebar.expander("Quantidade de parcelas:"):
    parcelas=st.slider("Selecione a quantidade de parcelas:",0,24,(0,24))

#FILTROS PARA MODIFICAR A TABELA
query = (
    dados["Produto"].isin(produto) &
    dados["Categoria do Produto"].isin(categorias) &
    dados["Preço"].between(preco[0], preco[1]) &
    dados["Frete"].between(frete[0], frete[1]) &
    dados["Data da Compra"].between(
        pd.to_datetime(data_compra[0]), pd.to_datetime(data_compra[1])
    ) &
    dados["Vendedor"].isin(vendedor) &
    dados["Local da compra"].isin(local_compra) &
    dados["Avaliação da compra"].between(avaliacao[0], avaliacao[1]) &
    dados["Tipo de pagamento"].isin(pagamento) &
    dados["Quantidade de parcelas"].between(parcelas[0], parcelas[1])
)




dados_filtrados=dados.copy()
dados_filtrados=dados_filtrados[query]
dados_filtrados=dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f"A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.")
st.markdown("Escreva um nome para o arquivo:")
coluna1,coluna2=st.columns(2)
with coluna1:
    nome_arquivo=st.text_input("",label_visibility="collapsed",value="dados")
    nome_arquivo+=".csv"
with coluna2:
    st.download_button("Fazer download da tabela em csv",data=converter_csv(dados_filtrados),file_name=nome_arquivo,mime="text/csv",on_click=mensagem_sucesso)
