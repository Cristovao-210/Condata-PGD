import streamlit as st 


# def gerar_relatorio():
    
    
#     with st.container():
#         st.subheader(" Informações Gerenciais ")
#         with st.expander(" Métricas ", True):
#             ...
#             # st.warning("Aqui ficarão as métricas")
#             # # Criar 3 colunas lado a lado
#             # col1, col2, col3 = st.columns(3)

#             # # Cada coluna recebe uma métrica
#             # col1.metric(label="Vendas", value="1500", delta="10%")            
#             # col2.metric(label="Clientes Ativos", value="320", delta="5")
#             # col3.metric(label="Satisfação", value="92%", delta="2%")
            
                            
  
#         with st.expander(" Tabelas ", True):
#             st.warning("Aqui ficarão as tabelas")
            
#         with st.expander(" Gráficos ", True):
#             st.warning("Aqui ficarão os gráficos")
    
import streamlit as st

def gerar_relatorio():
    with st.container():
        st.subheader(" Informações Gerenciais ")

        with st.expander(" Métricas ", True):
            # Criar 3 colunas
            col1, col2, col3 = st.columns(3)

            # Card 1
            with col1:
                st.markdown(
                    """
                    <div style="background-color:#f0f2f6;
                                padding:15px;
                                border-radius:10px;
                                text-align:center;">
                        <h3>💰 Vendas</h3>
                        <h2>1500</h2>
                        <p style="color:green;">+10%</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption("Comparado ao dia anterior")

            # Card 2
            with col2:
                st.markdown(
                    """
                    <div style="background-color:#f0f2f6;
                                padding:15px;
                                border-radius:10px;
                                text-align:center;">
                        <h3>👥 Clientes</h3>
                        <h2>320</h2>
                        <p style="color:green;">+5</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption("Novos clientes ativos")

            # Card 3
            with col3:
                st.markdown(
                    """
                    <div style="background-color:#f0f2f6;
                                padding:15px;
                                border-radius:10px;
                                text-align:center;">
                        <h3>⭐ Satisfação</h3>
                        <h2>92%</h2>
                        <p style="color:red;">-2%</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption("Pesquisa de feedback")