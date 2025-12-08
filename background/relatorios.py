import streamlit as st 


def gerar_relatorio():
    
    
    with st.container():
        st.subheader(" Informações Gerenciais ")
        with st.expander(" Métricas ", True):
            st.warning("Aqui ficarão as métricas")
            
        with st.expander(" Tabelas ", True):
            st.warning("Aqui ficarão as tabelas")
            
        with st.expander(" Gráficos ", True):
            st.warning("Aqui ficarão os gráficos")
    