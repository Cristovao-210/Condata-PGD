#===========Funções auxiliares===============
def retirar_espacos_colunas(df):
  for col in df[list(df)]:
    df[col] = df[col].str.strip()

def converter_colunas_str(df):
  return df.astype(str)

def retirar_codigo_orgao_coluna(txt: str):
  return str(int(str(txt[5:])))

def retirar_zero_a_esquerda(txt: str):
    return str(int(str(txt)))