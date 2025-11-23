from views.pages import navegacao, pg_carregar_arquvio, pg_validar_dados
from views.style import estilos
from background import background, carregar_dados, manipular_dados
import streamlit as st 

# Iniciar navegacao
aba_ativa = navegacao.barra_navegacao()

# Validar opções de navegacao
match aba_ativa:
    
    case "Upload":
        arquivo_carregado = pg_carregar_arquvio.carregar_arquivos(funcao_carregar_arquivos=background.carregar_arquivos_extrator)
        if arquivo_carregado:
            print("Carregou arquivos...") # Debug
            navegacao.btn_navegacao("active_tab", "Validação", "Validar Dados ➜","primary", True)
        
    case "Validação":
        dados = pg_validar_dados.validar_baixar_dados()
        if dados['dados_formatados']:
            css_table_html = estilos.estilo_tabela_download()
            navegacao.compontente_downoload_dados(background, dados['dados'], css_table_html)
            navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True)

