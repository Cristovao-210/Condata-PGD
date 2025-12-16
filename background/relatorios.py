import streamlit as st 


def gerar_relatorio():
    
    
    with st.container():
        st.subheader(" Informações Gerenciais ")
        with st.expander(" Métricas ", True):
            
            # st.warning("Aqui ficarão as métricas")
            # Criar 3 colunas lado a lado
            col1, col2, col3 = st.columns(3)

            # Cada coluna recebe uma métrica
            col1.metric(label="Total de Servidores", value="4976")            
            col2.metric(label="Servidores em PGD", value="1006")
            col3.metric(label="Percentual em PGD", value="20,2%")
            
                            
  
        with st.expander(" Tabelas ", True):
            st.warning("Aqui ficarão as tabelas")
            
        with st.expander(" Gráficos ", True):
            st.warning("Aqui ficarão os gráficos")
    
# import streamlit as st

# def gerar_relatorio():
#     with st.container():
#         st.subheader(" Informações Gerenciais ")

#         with st.expander(" Métricas ", True):
#             col1, col2, col3 = st.columns(3)

#             # Card 1 - Vendas (verde)
#             with col1:
#                 st.markdown(
#                     """
#                     <div style="background-color:#e6f4ea;
#                                 padding:15px;
#                                 border-radius:10px;
#                                 text-align:center;
#                                 border: 2px solid #2e7d32;">
#                         <h3 style="color:#2e7d32;">💰 Vendas</h3>
#                         <h2 style="color:#1b5e20;">1500</h2>
#                         <p style="color:#2e7d32;">+10%</p>
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )
#                 st.caption("Comparado ao dia anterior")

#             # Card 2 - Clientes (azul)
#             with col2:
#                 st.markdown(
#                     """
#                     <div style="background-color:#e3f2fd;
#                                 padding:15px;
#                                 border-radius:10px;
#                                 text-align:center;
#                                 border: 2px solid #1565c0;">
#                         <h3 style="color:#1565c0;">👥 Clientes</h3>
#                         <h2 style="color:#0d47a1;">320</h2>
#                         <p style="color:#1565c0;">+5</p>
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )
#                 st.caption("Novos clientes ativos")

#             # Card 3 - Satisfação (verde/azul misto)
#             with col3:
#                 st.markdown(
#                     """
#                     <div style="background-color:#f1f8e9;
#                                 padding:15px;
#                                 border-radius:10px;
#                                 text-align:center;
#                                 border: 2px solid #43a047;">
#                         <h3 style="color:#43a047;">⭐ Satisfação</h3>
#                         <h2 style="color:#1b5e20;">92%</h2>
#                         <p style="color:#c62828;">-2%</p>
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )
#                 st.caption("Pesquisa de feedback")