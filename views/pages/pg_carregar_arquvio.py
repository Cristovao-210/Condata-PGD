import streamlit as st
import pandas as pd


def carregar_arquivos(funcao_carregar_arquivos):
    
    # ABA: UPLOAD
    if st.session_state.active_tab == "Upload":
        st.header("1. Carregar Arquivos")

        # RECEBE POR PARÂMETRO A FUNÇÃO QUE CARREGA OS ARQUIVOS NA SESSÃO
        carga_arquivos_efetuada = funcao_carregar_arquivos()
        if carga_arquivos_efetuada:
            return True
        
