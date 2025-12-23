import gzip
import pandas as pd
import streamlit as st
from data._funcoes_auxiliares import *

# Gerar DataFrame com o conteúdo dos arquivos
def carregar_linhas_para_df(caminho_arquivo, nome_coluna="linha", encoding="utf-8"):
    """
    Lê um arquivo TXT ou TXT.GZ linha a linha
    e retorna um DataFrame com uma única coluna.
    """
    linhas = []

    # Se for .gz, usa gzip; caso contrário, open normal
    # if caminho_arquivo.endswith(".gz"):
    with gzip.open(caminho_arquivo, "rt", encoding=encoding) as f:
        for linha in f:
            linhas.append(linha.rstrip("\n"))
    # else:
    #     with open(caminho_arquivo, "r", encoding=encoding) as f:
    #         for linha in f:
    #             linhas.append(linha.rstrip("\n"))

    # Monta o DataFrame
    df = pd.DataFrame(linhas, columns=[nome_coluna])
    return df


def configurar_arquivos_extrator(arquivo, tipo_arquivo, encoding="utf-8"):
    
    '''
        arquivo: Recebe o caminho ou a refeência do arquivo.
        tipo_arquivo: 
            layout: Recebe o arquivo com o nome e o comprimento das colunas (arquivo.REF.gz)
                    Retorna uma lista com dicinários contendo o nome da coluna e o número de caracteres que cada uma ocupa.
            dados: Recebe o arquivo com os dados. Cada linha tem todas as colunas sem separador (arquivo.TXT.gz)
                   Retorna um dataFrame com uma coluna e cada linha contém as colunas compactadas.  

    '''

    match tipo_arquivo:
        
        case "layout":
            # Abrindo e tratando o conteúdo do arquivo
            try:
                df_layout = carregar_linhas_para_df(arquivo, nome_coluna="colunas_layout", encoding=encoding)
                if df_layout.empty:
                    st.warning("Arquivo de Layout lido, mas está vazio.")
                else:
                    # Criando lista com informações do Layout
                    lista_colunas = []
                    for linha in df_layout["colunas_layout"]:
                        lista_colunas.append({"nome_coluna": linha.replace(" ", "")[:-5], "num_caracteres":int(linha.replace(" ", "")[-4:])})
                    return lista_colunas
            except pd.errors.EmptyDataError:
                st.error("Erro: o arquivo está vazio ou sem colunas legíveis.")
                
                
        case "dados":
            # Abrindo e tratando o conteúdo do arquivo
            try:
                df_dados = carregar_linhas_para_df(arquivo, nome_coluna="dados_extraidos", encoding=encoding)
                if df_dados.empty:
                    st.warning("Arquivo de Dados lido, mas está vazio.")
                else:
                    # print("Gerando arquivo com dados extraídos...")
                    return df_dados
            except pd.errors.EmptyDataError:
                print("Erro: o arquivo está vazio ou sem colunas legíveis.")
                

def gerar_tabela_dados_extrator(lista_colunas, df_dados):
    
    '''
        lista_colunas: Informações do layout do arquivo
        df_dados: colunas de dados dos arquivos
        Transforma as colunas com os dados aglutinados em uma exibição tabular dos dados
    '''
    
    lista_tabela = []
    dicionario_linha_dados = {}
    for dados in df_dados['dados_extraidos']:
        linha_dados = dados
        # print(dados)
        for indice, coluna in enumerate(lista_colunas):
            dicionario_linha_dados[coluna['nome_coluna'].strip()] = linha_dados[:coluna['num_caracteres']].strip()
            # print(linha_dados[:coluna['num_caracteres']].strip(), coluna['num_caracteres'])
            linha_dados = linha_dados.replace(linha_dados[:coluna['num_caracteres']], "", 1).strip()
        lista_tabela.append(dicionario_linha_dados.copy())

    df_tabela_dados_extrator = pd.DataFrame(lista_tabela)
    # st.dataframe(df_tabela_dados_extrator, hide_index=True)
    return df_tabela_dados_extrator

#==================================== Configurações dados PGD
def criar_left_join_SIAPE_SIPORG(df_uorgs_siape, df_uorgs_SIORG, df_correcao_unidades_macro):
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
    # Fazendo o ajuste das unidades macros que foram corrigidas MANUALMENTE pela Laize
    for  sigla, uni_macro in zip(df_correcao_unidades_macro['sigla_unidade'], df_correcao_unidades_macro['unidade_macro']):
        for  sigla_copia, uni_macro_copia in zip(enumerate(df_SIAPE_left_join_SIORG['sigla_unidade']), enumerate(df_SIAPE_left_join_SIORG['unidade_macro'])):
            if sigla.strip() == sigla_copia[1].strip():
                df_SIAPE_left_join_SIORG.loc[sigla_copia[0], 'unidade_macro'] = uni_macro.strip()
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

def configurar_dados_arquivo_EXTRATOR(df_pgd_unb):#caminho_pgd_unb,
    # Carregando dados do PGD retirados do Extrator (HOD)
    df_pgd_unb = converter_colunas_str(df_pgd_unb)
    retirar_espacos_colunas(df_pgd_unb)
    df_pgd_unb["IT-CO-UORG-LOTACAO-SERVIDOR"] = df_pgd_unb["IT-CO-UORG-LOTACAO-SERVIDOR"].apply(lambda x: retirar_zero_a_esquerda(str(x)))
    df_pgd_unb["IT-CO-TIPO-PGD"] = df_pgd_unb["IT-CO-TIPO-PGD"].apply(lambda x: retirar_zero_a_esquerda(str(x)))
    df_pgd_unb = df_pgd_unb.rename(columns={"IT-CO-UORG-LOTACAO-SERVIDOR": "codigo_uorg_siape"})
    return df_pgd_unb

# Filtros Polare==========================================================================

def aplicar_filtros_planilha_POLARE(caminho_planilha_polare):
    # Carregando os dados da planilha
    df_polare = caminho_planilha_polare
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


def conferir_cadastro_servidores_POLARE(df_pgd_final, df_polare_lista_servidores):
    # Criando coluna para saber se está cadastrado no Sistema Polare
    df_pgd_final['cadastrado_no_polare'] = df_pgd_final['nome_servidor'].apply(lambda x: x.strip() in list(df_polare_lista_servidores)).map({True: "SIM", False: "NAO"})
    # Resetando o indice do DataFrame
    df_pgd_polare = df_pgd_final.reset_index(drop=True)
    return df_pgd_polare

# Verificar se os arquivos carregados são os necessários
def validar_colunas_dados(colunas_carregadas, fonte):
    match fonte:
        case "siape":
            colunas_esperadas = ["GR-MATRICULA",
                                "IT-NO-SERVIDOR",
                                "IT-CO-SITUACAO-SERVIDOR",
                                "IT-CO-GRUPO-OCOR-EXCLUSAO",
                                "IT-CO-GRUPO-CARGO-EMPREGO",
                                "IT-CO-CARGO-EMPREGO",
                                "IT-CO-UORG-LOTACAO-SERVIDOR",
                                "IT-CO-TIPO-PGD",
                                "IT-IN-PGD"]
            if colunas_carregadas:
                for indice, coluna_esperada in enumerate(colunas_esperadas):
                    if coluna_esperada not in colunas_carregadas[indice]["nome_coluna"]:
                        st.error("O Layout do arquivo não está de acordo com o esperado!")
                        st.write("Colunas Esperadas")
                        st.table(colunas_esperadas)
                        st.write("Colunas do arquivo carregado:")
                        st.table(colunas_carregadas)
                        return
                else:
                    # st.success("Layout dos dados do PGD: OK!", level="success")
                    pass
            else:
                return colunas_esperadas        
            
        case "polare":            
            colunas_esperadas = ["id",
                                    "ativo",
                                    "ano_referencia",
                                    "carga_horaria",
                                    "modelo_trabalho",
                                    "nome_servidor",
                                    "nome_unidade_localizacao",
                                    "nome_unidade_lotacao",
                                    "situacao",
                                    "nota_plano_individual",
                                    "motivo_nota",
                                    "mes_referencia_avaliacao",
                                    "ano_referencia_avaliacao",
                                    "nome_responsavel_avaliacao"]
            if colunas_carregadas:
                for coluna_esperada in colunas_esperadas:
                    if coluna_esperada not in colunas_carregadas:
                        st.error("O Layout da Planilha não está de acordo com o esperado!")
                        st.write("Colunas Esperadas")
                        st.table(colunas_esperadas)
                        st.write("Colunas da Planilha carregada:")
                        st.table(colunas_carregadas)
                        return
                else:
                    # st.success("Layout dos dados do POLARE: OK!", level="success")
                    pass
            else:
                return colunas_esperadas