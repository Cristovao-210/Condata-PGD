import streamlit as st 
import time

def buscar_emojis():
    return {
        "informatica": [
            "💻", "🖥️", "🖱️", "🖨️", "⌨️", "🖲️",
            "📱", "📲", "📟", "🕹️",
            "🌐", "📡", "🛜", "🔌", "🔋",
            "💾", "📀", "💿", "🧠", "🧮", "⚙️",
            "🛠️", "🔧", "🔨", "🧰",
            "🧑‍💻", "👨‍💻", "👩‍💻"
        ],
        "dados": [
            "🗄️", "🗃️", "🗂️", "💽",
            "📁", "📂", "📄", "📑",
            "💾", "🔄", "♻️"
        ],
        "navegacao": [
            "➡️", "⬅️", "⬆️", "⬇️",
            "↗️", "↘️", "↙️", "↖️",
            "🔀", "🔁", "🔄", "🔂",
            "⏺️", "⏹️", "⏯️", "⏭️", "⏮️",
            "📌", "📍",
            "🔽", "🔼",
            "▶️", "◀️",
            "🔍", "🔎"
        ],
        "seguranca": [
            "🔒", "🔓", "🔑", "🗝️", "🛡️"
        ],
        "infra": [
            "🗄️", "📡", "🛰️", "☁️",
            "🛠️", "🔧", "🔨", "⚙️", "🧰"
        ],
        "processamento": [
            "⚙️", "🔁", "🔄", "🔂",
            "🔗", "🧩", "🤖"
        ],
        "avisos": [
            "⚠️", "❗", "❕", "❌", "⛔",
            "🛑", "🐞", "🔍"
        ]
    }

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


def btn_navegacao(estado, destino, label, cor_btn, recarregar=False): # "Prosseguir ➜" "⬅ Voltar"
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
                if recarregar:
                    st.rerun()

    with col3:
        pass  
    

def compontente_downoload_dados(background, df, estilo_html):

    with st.expander("📥 Escolha o formato para download", True):
        # Criar 4 colunas para alinhar os botões
        col1, col2, col3, col4 = st.columns(4)

        with col1:
                background.baixar_df(df, "csv", "")

        with col2:
                background.baixar_df(df, "json", "")

        with col3:
                background.baixar_df(df, "xlsx", "")

        with col4:
                background.baixar_df(df, "html", estilo_html)
    st.markdown("---")
        