from data import carregar_dados, manipular_dados
from views.pages import navegacao, pg_carregar_arquvio, pg_mostrar_relatorios, pg_validar_dados
from views.style import estilos
from background import background
import streamlit as st 

# Iniciar navegacao
st.set_page_config(page_title="Consolidar Dados", page_icon="🔄")
aba_ativa = navegacao.barra_navegacao()

# Validar opções de navegacao
match aba_ativa:
    
    case "Upload":
            # Navegação local (provisória)
            tab_siape, tab_polare = st.tabs(["Dados do SIAPE", "Dados do Polare"])
            mostrar_msg_alerta = True
            with tab_siape:
                arquivo_carregado = pg_carregar_arquvio.carregar_arquivos(funcao_carregar_arquivos=background.carregar_arquivos_extrator, 
                                                            descricao_carregamento="1. Carregar dados do PGD")
                if arquivo_carregado:
                    mostrar_msg_alerta = False
                    st.info(":information_source: Selecione a aba Dados do Polare. ➜")
            if arquivo_carregado or mostrar_msg_alerta:
                with tab_polare:
                    if mostrar_msg_alerta:
                        st.warning("⚠️ Primeiro carrege os dados do PGD vindos do SIAPE.")
                    else:
                        planilha_cerregada = pg_carregar_arquvio.carregar_arquivos(funcao_carregar_arquivos=background.carregar_planilha_polare, 
                                                                            descricao_carregamento="2. Carregar dados do Polare")
                        if planilha_cerregada:
                            navegacao.btn_navegacao("active_tab", "Validação", "Validar Dados ➜","primary", True, False)
                    
    case "Validação":
        dados = pg_validar_dados.validar_baixar_dados()
        if dados:
            if dados['dados_carregados']:
                try:
                    # Descompatando e configurando arquivos do extrator
                    lista_colunas = manipular_dados.configurar_arquivos_extrator(dados["layout_extrator"], "layout")
                    df_dados = manipular_dados.configurar_arquivos_extrator(dados["dados_extrator"], "dados")
                    df_dados_EXTRATOR = manipular_dados.gerar_tabela_dados_extrator(lista_colunas=lista_colunas, df_dados=df_dados)
                    # Verificando se o arquivo carregado está com as colunas corretas
                    manipular_dados.validar_colunas_dados(lista_colunas, "siape")
                    df_dados_EXTRATOR = manipular_dados.configurar_dados_arquivo_EXTRATOR(df_pgd_unb=df_dados_EXTRATOR)
                    # carregar tabelas auxiliares
                    df_uorgs_siape = carregar_dados.carregar_uorgs_siape(caminho_uorgs_siape="data/data_files/UORGS-SIAPE.csv")
                    df_uorgs_SIORG = carregar_dados.carregar_uorgs_SIORG(caminho_uorgs_SIORG="data/data_files/UORGS-SIORG.csv")
                    df_correcao_unidades_macro = carregar_dados.carregar_acerto_nome_unidades_macro(caminho_acerto_nome_unidades="data/data_files/correcao_unidades_macro.xlsx")
                    df_SIAPE_left_join_SIORG = manipular_dados.criar_left_join_SIAPE_SIPORG(df_uorgs_siape=df_uorgs_siape, df_uorgs_SIORG=df_uorgs_SIORG, df_correcao_unidades_macro=df_correcao_unidades_macro)
                    # Tratar nome das uorgs
                    df_pgd_final = manipular_dados.anexar_uorgs_tabela_PGD(df_pgd_unb=df_dados_EXTRATOR, df_SIAPE_left_join_SIORG=df_SIAPE_left_join_SIORG)
                    # Tratar planilha do Polare
                    df_planilha_polare = dados['dados_polare']
                    manipular_dados.validar_colunas_dados(list(df_planilha_polare), "polare")
                    df_polare_lista_servidores = manipular_dados.aplicar_filtros_planilha_POLARE(caminho_planilha_polare=df_planilha_polare)
                    # Consolidar dados do SIAPE com tabela do POLARE
                    df_pgd_polare = manipular_dados.conferir_cadastro_servidores_POLARE(df_pgd_final=df_pgd_final, df_polare_lista_servidores=df_polare_lista_servidores)
                    # Opções de download                    
                    navegacao.compontente_downoload_dados(background, df_pgd_polare, estilos.estilo_tabela_download())
                    # Exibir dados consolidadeos
                    st.dataframe(df_pgd_polare)
                    # navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True, True)
                except:
                    navegacao.btn_navegacao("active_tab", "Upload", "⬅ Carregar novos arquivos","primary", True, True)
                    
    case "Relatórios":
        pg_mostrar_relatorios.gerar_relatorio()

