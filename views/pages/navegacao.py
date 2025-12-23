import streamlit as st 
import time


def barra_navegacao():
    
    # =======================================
    # Inicialização do estado
    # =======================================
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Upload"

    # =======================================
    # Barra de navegação horizontal (abas)
    # =======================================
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            # Aba Upload
            if st.button(
                "📁 Carregar dados",
                use_container_width=True,
                type=("primary" if st.session_state.active_tab == "Upload" else "secondary")
            ):
                st.session_state.active_tab = "Upload"
                st.rerun()

        with col2:
            # Aba Validação/visualização
            if st.button(
                "📄 Visualizar dados",
                use_container_width=True,
                type=("primary" if st.session_state.active_tab == "Validação" else "secondary")
            ):
                st.session_state.active_tab = "Validação"
                st.rerun()
                
        with col3:
            # Aba Relatorios
            if st.button(
                "📊 Relatórios",
                use_container_width=True,
                type=("primary" if st.session_state.active_tab == "Relatórios" else "secondary")
            ):
                st.session_state.active_tab = "Relatórios"
                st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    return st.session_state.active_tab

def centralizar_texto(txt):
    st.markdown(f"""<p style="text-align: center;">{txt}</p>""", unsafe_allow_html=True)

def centralizar_titulo(titulo):
    st.markdown(f"""<h3 style="font-weight: bold; text-align: center;">{titulo}</h3>""", unsafe_allow_html=True)
    

def limpar_navegacao():
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()  

def btn_navegacao(estado, destino, label, cor_btn, recarregar=False, resetar=False): # "Prosseguir ➜" "⬅ Voltar"
    # Separar por colunas para centralizar o botão
    col1, col2, col3 = st.columns([0.5, 0.8, 0.1])                
    
    with col1:
        pass
    
    with col2:
        if st.button(label, type=cor_btn):  
            # Efeito de carregamento
            with st.spinner("Processando solicitação..."):
                time.sleep(3)
                st.session_state[estado] = destino
                if resetar:
                    limpar_navegacao()                    
                if recarregar: 
                    st.rerun()

    with col3:
        pass  
    

def compontente_downoload_dados(background, df, estilo_html):

    with st.expander("📥 Escolha o formato para download", False):
        # Criar 4 colunas para alinhar os botões
        col1, col2, col3, col4 = st.columns(4)

        with col1:
                background.baixar_df(df, "csv", "")
                limpar_navegacao()  

        with col2:
                background.baixar_df(df, "json", "")
                limpar_navegacao()

        with col3:
                background.baixar_df(df, "xlsx", "")
                limpar_navegacao()

        with col4:
                background.baixar_df(df, "html", estilo_html)
                limpar_navegacao()
    # st.markdown("---")
        

def btn_switch_paginas_app(label_btn, pagina_destino):
    
    st.markdown("---")
    col_1_btn, col_2_btn, col_3_btn = st.columns(3)
    with col_1_btn:
        pass
    with col_2_btn:
        if st.button(f"{label_btn}", type="primary"):
            st.switch_page(f"{pagina_destino}")
    with col_3_btn:
        pass
    st.markdown("---")