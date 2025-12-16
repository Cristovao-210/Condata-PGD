import pandas as pd 
from data.funcoes_auxiliares import *


def carregar_uorgs_siape(caminho_uorgs_siape):
    # Carregando dados das UORGS do SIAPE
    df_uorgs_siape = pd.read_csv(caminho_uorgs_siape, sep=",", encoding="utf-8")
    df_uorgs_siape = converter_colunas_str(df_uorgs_siape)
    retirar_espacos_colunas(df_uorgs_siape)
    df_uorgs_siape = df_uorgs_siape.rename(columns={
        "GR-IDENTIFICACAO-UORG": "codigo_uorg_siape",
        "IT-NO-UNIDADE-ORGANIZACIONAL": "nome_uorg_siape",
        "IT-SG-UNIDADE-ORGANIZACIONAL": "sigla_uorg_siape",
        "IT-CO-ORGAO-SIORG": "codigo_orgao",
        "IT-CO-UORG-SIORG": "codigo_siorg_uorg"
    })
    df_uorgs_siape["codigo_uorg_siape"] = df_uorgs_siape["codigo_uorg_siape"].apply(lambda x: retirar_codigo_orgao_coluna(x))
    return df_uorgs_siape


def carregar_uorgs_SIORG(caminho_uorgs_SIORG):
    # Carregando dados das UORGS do SIORG (DPO)
    df_uorgs_SIORG = pd.read_csv(caminho_uorgs_SIORG, sep=";", encoding="utf-8")
    df_uorgs_SIORG = converter_colunas_str(df_uorgs_SIORG)
    retirar_espacos_colunas(df_uorgs_SIORG)
    df_uorgs_SIORG = df_uorgs_SIORG.rename(columns={"codigo": "codigo_siorg_uorg"})
    return df_uorgs_SIORG

def carregar_acerto_nome_unidades_macro(caminho_acerto_nome_unidades):
    # Carregando dados para acerto no nome das uniades e unidades macro
    df_correcao_unidades_macro = pd.read_excel(caminho_acerto_nome_unidades)
    df_correcao_unidades_macro = converter_colunas_str(df_correcao_unidades_macro)
    retirar_espacos_colunas(df_correcao_unidades_macro)
    return df_correcao_unidades_macro
        
