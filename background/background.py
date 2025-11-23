import streamlit as st
import pandas as pd
from io import BytesIO


# ========================
def carregar_arquivos_extrator():
    
    # Componente para carregar os arquivos
    arquivos = st.file_uploader(
        "Escolha exatamente 2 arquivos (.REF.gz e .TXT.gz)",
        type=["gz"],
        accept_multiple_files=True,
        key="upload_arquivos"
    )
    # Ações de validação após o carregamento do arquivo
    if arquivos:
        # Validar quantidade
        if len(arquivos) != 2:
            st.error("❌ Você deve carregar **exatamente 2 arquivos**: um .REF.gz e um .TXT.gz.")
        else:
            # Identificar arquivos
            arquivo_layout = None
            arquivo_dados = None

            for arquivo in arquivos:
                nome = arquivo.name.upper()

                if nome.endswith("REF.GZ"):
                    arquivo_layout = arquivo
                elif nome.endswith("TXT.GZ"):
                    arquivo_dados = arquivo

            # Verificar se ambos foram encontrados
            if arquivo_layout is None or arquivo_dados is None:
                st.error("""
                ❌ Arquivos inválidos.  
                Você deve enviar **exatamente 2 arquivos**:
                - Um que termine com **REF.gz** (layout)  
                - Um que termine com **TXT.gz** (dados)  
                """)
            else:
                st.success("✔️ Arquivos carregados com sucesso!")
                st.session_state["arquivo_layout"] = arquivo_layout
                st.session_state["arquivo_dados"] = arquivo_dados
                print(arquivo_dados.name,"\n",arquivo_layout.name) # Debug
                return True
    


def reset_app():
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()


def baixar_df(df: pd.DataFrame, formato: str, estilo_html: str):
    formato = formato.lower()

    if formato == "csv":
        data = df.to_csv(index=False).encode("utf-8")
        mime = "text/csv"
        nome_arquivo = "dados.csv"

    elif formato == "json":
        data = df.to_json(orient="records", force_ascii=False).encode("utf-8")
        mime = "application/json"
        nome_arquivo = "dados.json"

    elif formato == "html":
        html_base = df.to_html(index=False)
        # Pega o html gerado pelo pandas e associa ao estilo css preparado
        data = (estilo_html + html_base).encode("utf-8")
        mime = "text/html"
        nome_arquivo = "dados.html"

    elif formato == "xlsx":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="dados")
        data = buffer.getvalue()
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        nome_arquivo = "dados.xlsx"

    else:
        st.error("❌ Formato não suportado.")
        return
    # Botão para baixar no formato escolhido
    try:
       
        st.download_button(
            label=f"📥 {formato.upper()}",
            data=data,
            file_name=nome_arquivo,
            mime=mime,
            use_container_width=True
        )

    except:
        st.error("Erro no Download do arquivo... Refaça a operação.")


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