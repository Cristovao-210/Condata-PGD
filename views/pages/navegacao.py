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
        col1, col2 = st.columns([1, 1])

        with col1:
            # Aba Upload
            if st.button(
                "📁 Upload",
                use_container_width=True,
                type=("primary" if st.session_state.active_tab == "Upload" else "secondary")
            ):
                st.session_state.active_tab = "Upload"
                st.rerun()

        with col2:
            # Aba Validação
            if st.button(
                "📊 Validação",
                use_container_width=True,
                type=("primary" if st.session_state.active_tab == "Validação" else "secondary")
            ):
                st.session_state.active_tab = "Validação"
                st.rerun()

    st.markdown("---")
    return st.session_state.active_tab


def btn_navegacao(estado):
    # Separar por colunas para centralizar o botão
                col1, col2, col3 = st.columns([0.5, 0.8, 0.1])                
                
                with col1:
                    pass
                
                with col2:
                  if st.button("📄 Formatar Dados"):
                        
                    st.session_state[estado]
                    st.session_state["pagina2"] = 1
                    # Efeito de carregamento
                    with st.spinner("Carregando dados..."):
                        time.sleep(3)
                    if st.button("Prosseguir ➜", type="primary"):
                        st.session_state.active_tab = "Validação"
                        st.rerun()

                with col3:
                    pass    