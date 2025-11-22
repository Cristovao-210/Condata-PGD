import streamlit as st
import pandas as pd



def carregar_arquivos():
    
    # =======================================
    # ABA: UPLOAD
    # =======================================
    if st.session_state.active_tab == "Upload":
        st.header("1. Carregar Arquivo")

        uploaded = st.file_uploader(
            "Escolha um arquivo .txt",
            type=["txt"],
            key="file_input"
        )

        if uploaded:
            st.session_state["raw_file"] = uploaded.read().decode("utf-8")
            st.success("Arquivo carregado com sucesso!")

            if st.button("Prosseguir ➜", type="primary"):
                st.session_state.active_tab = "Validação"
                st.rerun()
            
