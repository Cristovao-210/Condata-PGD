import gzip
import pandas as pd
import streamlit as st

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
                    st.warning("Arquivo lido, mas está vazio.")
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
                    st.warning("Arquivo lido, mas está vazio.")
                else:
                    print("Gerando arquivo com dados extraídos...")
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