import streamlit as st
import pandas as pd


def carregar_arquivos(funcao_carregar_arquivos, descricao_carregamento):
    
    '''
    Docstring for carregar_arquivos
    
    :param funcao_carregar_arquivos: Recebe a função que fará o processamento do arquivo.
    :param descricao_carregamento: "1. Carregar dados do PGD" ou "2. Carregar dados do Polare"
    '''
    
    # ABA: UPLOAD
    if st.session_state.active_tab == "Upload":
        st.header(descricao_carregamento)

        # RECEBE POR PARÂMETRO A FUNÇÃO QUE CARREGA OS ARQUIVOS NA SESSÃO
        carga_arquivos_efetuada = funcao_carregar_arquivos()
        if carga_arquivos_efetuada:
            return True
    
        
