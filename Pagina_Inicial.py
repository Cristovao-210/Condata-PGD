import streamlit as st
from background import background
from views.pages import navegacao
from data import manipular_dados

st.set_page_config(page_title="Condata-PGD", page_icon="💾")

st.markdown("""<h3 style="font-weight: bold; text-align: center;">💾 Condata-PGD</h3>""", unsafe_allow_html=True)
st.markdown("""<p style="text-align: center;">Consolidação dos dados do Programa de Gestão e Desenvolvimento (PGD-UnB)</p><br>""", unsafe_allow_html=True)

# Navegação local (provisória)
tab_informacoes, tab_tutorial, tab_baixar_arquivos, tab_acessar_consolidacao = st.tabs(["Informações de uso", 
                                                                                        "Tutoriais para o Extrator SIAPE", 
                                                                                        "Macros do SIAPE para Download",
                                                                                        "Página de consolidação"])

with tab_informacoes:
    st.write(
    '''
    Para consolidadção dos dados do PGD é necessário que alguns critérios sejam respeitados
    
        Após a extração dos dados no Extrator de dados do SIAPE:
            1 - Carregar os 2 arquivos formnecidos pela extrator: (.REF.gz) e (.TXT.gz)
            2 - Os arquivos devem conter exatamente as colunas que serão listadas abaixo.
        Após a extração da planilha com os dados do sistema Polare:
            1 - Certificar-se de que a planilha é o mais recente possível.
            2 - A planilha deve conter exatamente as colunas que serão listadas abaixo.
    ''')
    with st.expander(" 📑 Clique para ver as listas de colunas esperadas nos arquivos", False):
        col_siape, col_polare = st.columns(2)
        with col_siape:
            st.text("Colunas esperadas nos arquivos do extrator")
            st.write(manipular_dados.validar_colunas_dados(colunas_carregadas="", fonte="siape"))
        with col_polare:
            st.text("Colunas esperadas na planilha do Polare")
            st.write(manipular_dados.validar_colunas_dados(colunas_carregadas="", fonte="polare"))      
    background.mostrar_video_tutorial(titutlo_video="🖥️ Visão geral das funcionalidades do **Condata-PGD**", url_video="https://www.youtube.com/watch?v=GAS6k0nmZ8U")
            

with tab_tutorial:
    navegacao.centralizar_texto("Vídeos demonstrando como realizar a extração dos dados do PGD no SIAPE")
    background.mostrar_video_tutorial(titutlo_video="🖥️ Extração de dados do PGD no SIAPE - PARTE 1", url_video="https://www.youtube.com/watch?v=moNns3PlJpg")
    background.mostrar_video_tutorial(titutlo_video="🖥️ Extração de dados do PGD no SIAPE - PARTE 2", url_video="https://www.youtube.com/watch?v=FmffLwtrbdA")

with tab_baixar_arquivos:
    navegacao.centralizar_texto("Para facilitar a extração dos dados no SIAPE é possível utilizar uma automação via macro")
    background.baixar_macros_siape("background/macros_siape/extracao_pgd_unb.mac", "extracao_pgd_unb.mac")
    navegacao.centralizar_texto("Tutoriais de como utilizar e criar macros no SIAPE (HOD-3270)")
    background.mostrar_video_tutorial(titutlo_video="🖥️ UTILIZANDO macros para extração de dados no SIAPE - PARTE 1", url_video="https://www.youtube.com/watch?v=37NXFUGq3dw")
    background.mostrar_video_tutorial(titutlo_video="🖥️ CRIANDO macros para extração de dados no SIAPE - PARTE 2", url_video="https://www.youtube.com/watch?v=J1f_b_Wg4JE")
    
with tab_acessar_consolidacao:
    navegacao.centralizar_texto("<br>Use a barra lateral para acessar a página de consolidação dos dados ou clique no botão abaixo.")
    navegacao.btn_switch_paginas_app(label_btn="Consolidar dados ->", pagina_destino="pages/Consolidar_Dados.py")
    
    