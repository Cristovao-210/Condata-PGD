import streamlit as st
import pandas as pd
from io import BytesIO


def reset_app():
    st.session_state.clear()
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()


def baixar_df(df: pd.DataFrame, formato: str, estilo_html: str):
    formato = formato.lower()

    if formato == "csv":
        data = df.to_csv(index=False).encode("latin1")
        mime = "text/csv"
        nome_arquivo = "dados.csv"

    elif formato == "json":
        data = df.to_json(orient="records", force_ascii=False).encode("utf-8")
        mime = "application/json"
        nome_arquivo = "dados.json"

    elif formato == "html":
        html_base = df.to_html(index=False)
        # Pega o html gerado pelo pandas e associa ao estilo css preparado
        data = (estilo_html + html_base).encode("latin1")
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
