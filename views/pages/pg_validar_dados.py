import streamlit as st
import pandas as pd


def validar_baixar_dados():
    
    # ABA: VALIDAÇÃO
    st.header("2. Validar Dados")
    
    if "raw_file" not in st.session_state:
        st.warning("⚠️ Nenhum arquivo foi carregado ainda. Volte para a página inicial.")
    else:
        lines = st.session_state["raw_file"].split("\n")
        df = pd.DataFrame({"linhas": lines})

        st.dataframe(df)

        df_html = df.to_html(index=False)

        return {'dados': df, 'dados_formatados': True}