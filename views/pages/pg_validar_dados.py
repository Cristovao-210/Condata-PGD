import streamlit as st
import pandas as pd


def validar_baixar_dados():
    
    # ABA: VALIDAÇÃO
    st.header(" Visualizar / baixar Dados")
    
    if "arquivo_layout" not in st.session_state and "arquivo_dados" not in st.session_state and not "planilha_polare" in st.session_state:
        st.warning("⚠️ Os arquivos necessários ainda não foram carregados. Volte para a página de carregamento.")
    else:
        try:
            # Retornando dados da sessão
            _planilha = st.session_state["planilha_polare"]
            _layout = st.session_state["arquivo_layout"]
            _dados = st.session_state["arquivo_dados"]
            return {'dados_polare': _planilha,  "layout_extrator": _layout, "dados_extrator": _dados, 'dados_carregados': True}
        except:
            st.error("❌ Não foram carregados todos os arquivos necesários. Refaça a operação!")