import streamlit as st
import pandas as pd 
import time

def retirar_espacos_colunas(df):
  for col in df[list(df)]:
    df[col] = df[col].str.strip()

def converter_colunas_str(df):
  return df.astype(str)

def retirar_codigo_orgao_coluna(txt: str):
  return str(int(str(txt[5:])))

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


def criar_left_join_SIAPE_SIPORG(df_uorgs_siape, df_uorgs_SIORG):
    # Criando tabela de UORGS (Com e sem correspondência)
    df_SIAPE_left_join_SIORG = pd.merge(df_uorgs_siape, df_uorgs_SIORG, on="codigo_siorg_uorg", how="left")
    df_SIAPE_left_join_SIORG = df_SIAPE_left_join_SIORG.drop(columns=["codigo_orgao", "codigo_siorg_uorg"])
    # Criando coluna que identifica se o nome é SIORG ou SIAPE
    df_SIAPE_left_join_SIORG['nome_siorg'] = df_SIAPE_left_join_SIORG['sigla_unidade'].isna().map({True: "NAO", False: "SIM"})
    # Preenchendo o nome das unidades e siglas quando não houver correspondência SIORG
    # Quando não há correspondência recebe o nome que estava no SIAPE mesmo
    filtro_nome_unidade_isna = df_SIAPE_left_join_SIORG['nome_unidade'].isna()
    # df_SIAPE_left_join_SIORG['nome_unidade'][filtro_nome_unidade_isna] = df_SIAPE_left_join_SIORG['nome_uorg_siape']
    df_SIAPE_left_join_SIORG.loc[filtro_nome_unidade_isna, 'nome_unidade'] = df_SIAPE_left_join_SIORG['nome_uorg_siape']
    filtro_sigla_unidade_isna = df_SIAPE_left_join_SIORG['sigla_unidade'].isna()
    # df_SIAPE_left_join_SIORG['sigla_unidade'][filtro_sigla_unidade_isna] = df_SIAPE_left_join_SIORG['sigla_uorg_siape']
    df_SIAPE_left_join_SIORG.loc[filtro_sigla_unidade_isna, 'sigla_unidade'] = df_SIAPE_left_join_SIORG['sigla_uorg_siape']
    filtro_unidade_macro_isna = df_SIAPE_left_join_SIORG['unidade_macro'].isna()
    # df_SIAPE_left_join_SIORG['unidade_macro'][filtro_unidade_macro_isna] = df_SIAPE_left_join_SIORG['sigla_uorg_siape']
    df_SIAPE_left_join_SIORG.loc[filtro_unidade_macro_isna, 'unidade_macro'] = df_SIAPE_left_join_SIORG['sigla_uorg_siape']
    # Excluindo colunas com nomenclaturas vindas do SIAPE
    df_SIAPE_left_join_SIORG = df_SIAPE_left_join_SIORG.drop(columns=["nome_uorg_siape", "sigla_uorg_siape"])
    return df_SIAPE_left_join_SIORG


def anexar_uorgs_tabela_PGD(df_pgd_unb, df_SIAPE_left_join_SIORG):
    # Anexando setores (UORGS) a tabela do PGD (com e sem correspondência)
    df_pgd_left_join = pd.merge(df_pgd_unb, df_SIAPE_left_join_SIORG, on="codigo_uorg_siape", how="left")
    df_pgd_left_join = converter_colunas_str(df_pgd_left_join)
    retirar_espacos_colunas(df_pgd_left_join)

    # Alterar nome das colunas que irão ficar no df
    df_pgd_left_join = df_pgd_left_join.rename(columns={
        "GR-MATRICULA": "matricula_siape",
        "IT-NO-SERVIDOR": "nome_servidor",
        "IT-CO-GRUPO-CARGO-EMPREGO": "grupo_cargo",
        "IT-CO-TIPO-PGD": "codigo_modalidade_pgd",
        "IT-IN-PGD": "participacao_pgd"
    })
    # Formatar matricula siape
    df_pgd_left_join["matricula_siape"] = df_pgd_left_join["matricula_siape"].apply(lambda x: retirar_codigo_orgao_coluna(x))
    # Dropar as colunas desnessárias
    df_pgd_left_join = df_pgd_left_join.drop(columns=["IT-CO-SITUACAO-SERVIDOR", "IT-CO-GRUPO-OCOR-EXCLUSAO", "IT-CO-CARGO-EMPREGO"])
    # Criar coluna nome modalidade com base no código da it-co-tipo-pgd
    df_pgd_left_join["nome_modalidade_pgd"] = df_pgd_left_join["codigo_modalidade_pgd"].map({
        "0": "NAO PARTICIPA DO PGD",
        "1": "PRESENCIAL",
        "2":"TELETRABALHO PARCIAL",
        "3": "TELETRABALHO INTEGRAL",
        "4": "TELE. EXTERIOR (DEC. 11.072/22, ART. 12, VIII - SUBSTITUICAO)",
        "5": "TELE. EXTERIOR (DEC. 11.072/22, ART. 12, §7° - DISCRICIONARIA)"
    })
    # Na coluna it-in-pgd substituir s = sim e n = nao
    df_pgd_left_join["participacao_pgd"] = df_pgd_left_join["participacao_pgd"].map({"S": "SIM", "N": "NAO"})
    # Mostrar resultado
    # df_pgd_left_join.head(100)

    # Finalizando edição e gerando planilha Excel
    colunas_df_pgd_final = ['matricula_siape',
    'nome_servidor',
    'grupo_cargo',
    'nome_unidade',
    'sigla_unidade',
    'unidade_macro',
    'nome_siorg',
    'participacao_pgd',
    'codigo_modalidade_pgd',
    'nome_modalidade_pgd']
    
    df_pgd_final = df_pgd_left_join[colunas_df_pgd_final].sort_values('nome_servidor')
    return df_pgd_final

def aplicar_filtros_planilha_POLARE(caminho_planilha_polare):
    # Carregando os dados da planilha
    df_polare = pd.read_excel(caminho_planilha_polare)
    df_polare = df_polare.astype(str)
    retirar_espacos_colunas(df_polare)
    # filtros a serem utilizados
    # Coluna "ano_referencia": 2025
    filtro_ano_referencia = (df_polare["ano_referencia"] == "2025")
    # Coluna "ativo": VERDADEIRO
    filtro_coluna_ativo = (df_polare["ativo"] == "True")
    # Coluna "situacao": ['HOMOLOGADO', 'PENDENTE_HOMOLOGACAO','CADASTRADO', 'NECESSITA_CORRECAO'] df_polare['situacao'].unique()
    filtro_coluna_situacao = (df_polare['situacao'] != 'FINALIZADO')
    # DataFrame filtrado
    df_polare_lista_servidores =  df_polare['nome_servidor'][filtro_ano_referencia & filtro_coluna_ativo & filtro_coluna_situacao].drop_duplicates()
    return df_polare_lista_servidores