import streamlit as st 


def gerar_relatorio():
    
    
    with st.container():
        st.subheader(" Informações Gerenciais ")
        with st.expander(" Métricas ", True):
            
            st.warning("Aqui ficarão as métricas")
            # # Criar 3 colunas lado a lado
            # col1, col2, col3 = st.columns(3)

            # # Cada coluna recebe uma métrica
            # col1.metric(label="Total de Servidores", value="4976")            
            # col2.metric(label="Servidores em PGD", value="1006")
            # col3.metric(label="Percentual em PGD", value="20,2%")
            
                            
  
        with st.expander(" Tabelas ", True):
            st.warning("Aqui ficarão as tabelas")
            
        with st.expander(" Gráficos ", True):
            st.warning("Aqui ficarão os gráficos")