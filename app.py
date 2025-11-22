from views.pages import navegacao, pg_carregar_arquvio, pg_validar_dados
import streamlit as st 



aba_ativa = navegacao.barra_navegacao()

match aba_ativa:
    case "Upload":
        pg_carregar_arquvio.carregar_arquivos()
        print(aba_ativa)
    case "Validação":
        pg_validar_dados.validar_baixar_dados()
        print(aba_ativa)





