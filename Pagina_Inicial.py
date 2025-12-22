import streamlit as st
from background import background
from views.pages import navegacao

st.set_page_config(page_title="Condata-PGD", page_icon="💾")

# st.subheader("💾 Condata-PGD")
st.markdown("""<h3 style="font-weight: bold; text-align: center;">💾 Condata-PGD</h3>""", unsafe_allow_html=True)
st.markdown("""<p style="text-align: center;">Consolidação dos dados do Programa de Gestão e Desenvolvimento (PGD-UnB)</p><br>""", unsafe_allow_html=True)

# Navegação local (provisória)
tab_informacoes, tab_tutorial, tab_baixar_arquivos = st.tabs(["Informações de uso", "Tutoriais para o Extrator SIAPE", "Macros do SIAPE para Download"])

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
    col_siape, col_polare = st.columns(2)
    with col_siape:
        st.text("Colunas esperadas nos arquivos do extrator")
        ["GR-MATRICULA",
        "IT-NO-SERVIDOR",
        "IT-CO-SITUACAO-SERVIDOR",
        "IT-CO-GRUPO-OCOR-EXCLUSAO",
        "IT-CO-GRUPO-CARGO-EMPREGO",
        "IT-CO-CARGO-EMPREGO",
        "IT-CO-UORG-LOTACAO-SERVIDOR",
        "IT-CO-TIPO-PGD",
        "IT-IN-PGD"]
    with col_polare:
        st.text("Colunas esperadas na planilha do Polare")
        ["id",
        "ativo",
        "ano_referencia",
        "carga_horaria",
        "modelo_trabalho",
        "nome_servidor",
        "nome_unidade_localizacao",
        "nome_unidade_lotacao",
        "situacao",
        "nota_plano_individual",
        "motivo_nota",
        "mes_referencia_avaliacao",
        "ano_referencia_avaliacao",
        "nome_responsavel_avaliacao"]

with tab_tutorial:
    navegacao.centralizar_texto("Vídeo demonstrando como realizar a extração no SIAPE")

with tab_baixar_arquivos:
    navegacao.centralizar_texto("Para facilitar a extração dos dados no SIAPE é possível utilizar uma automação via macro")
    background.baixar_macros_siape("background/macros_siape/extrator_pgd_unb.mac", "extrator_pgd_unb.mac")
    navegacao.centralizar_texto("Segue um breve vídeo de como utilizar macros no SIAPE (HOD-3270)")
    
    