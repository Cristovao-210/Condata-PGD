from views.pages import navegacao, pg_carregar_arquvio, pg_validar_dados
from background import background, carregar_dados, manipular_dados
import streamlit as st 



aba_ativa = navegacao.barra_navegacao()

match aba_ativa:
    case "Upload":
        arquivo_carregado = pg_carregar_arquvio.carregar_arquivos()
        if arquivo_carregado:
            navegacao.btn_navegacao("active_tab", "Validação", "Validar Dados ➜","primary", True)
        print(aba_ativa)
    case "Validação":
        dados = pg_validar_dados.validar_baixar_dados()
        if dados['dados_formatados']:
            navegacao.compontente_downoload_dados(background, dados['dados'], "")
            navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True)
        print(aba_ativa)





