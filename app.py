from views.pages import navegacao, pg_carregar_arquvio, pg_validar_dados
from views.style import estilos
from background import background, carregar_dados, manipular_dados, relatorios
import streamlit as st 

# Iniciar navegacao
aba_ativa = navegacao.barra_navegacao()

# Validar opções de navegacao
match aba_ativa:
    
    case "Upload":
        arquivo_carregado = pg_carregar_arquvio.carregar_arquivos(funcao_carregar_arquivos=background.carregar_arquivos_extrator, 
                                                                  descricao_carregamento="1. Carregar dados do PGD")
        if arquivo_carregado:
            # print("Carregou arquivos...") # Debug
            planilha_cerregada = pg_carregar_arquvio.carregar_arquivos(funcao_carregar_arquivos=background.carregar_planilha_polare, 
                                                                  descricao_carregamento="2. Carregar dados do Polare")
            if planilha_cerregada:
                navegacao.btn_navegacao("active_tab", "Validação", "Validar Dados ➜","primary", True, False)
        
    case "Validação":
        dados = pg_validar_dados.validar_baixar_dados()
        if dados:
            if dados['dados_carregados']:
                try:
                    lista_colunas = manipular_dados.configurar_arquivos_extrator(dados["layout_extrator"], "layout")
                    df_dados = manipular_dados.configurar_arquivos_extrator(dados["dados_extrator"], "dados")
                    df_dados_EXTRATOR = manipular_dados.gerar_tabela_dados_extrator(lista_colunas=lista_colunas, df_dados=df_dados)
                    df_planilha_polare = st.session_state["planilha_polare"]
                    st.dataframe(df_planilha_polare) # debug
                    navegacao.compontente_downoload_dados(background, df_dados_EXTRATOR, estilos.estilo_tabela_download())
                    # navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True, True)
                except:
                    navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True, True)
                    
           
        
    case "Relatórios":
        relatorios.gerar_relatorio()

