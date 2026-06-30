import pandas as pd
import mysql.connector

# =========================
# LER EXCEL
# =========================

df = pd.read_excel("vendas.xlsx")

# =========================
# LIMPEZA DOS DADOS
# =========================

# Remove linhas totalmente vazias
df = df.dropna(how="all")

# Remove espaços extras nos nomes das colunas
df.columns = df.columns.str.strip()

# Remove espaços extras dos textos
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

# Remove IDs duplicados no pandas
df = df.drop_duplicates(subset=["id"])

# Substitui NaN por None
df = df.where(pd.notnull(df), None)

print(df.head())

# =========================
# CONEXÃO MYSQL
# =========================

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senha",
    database="teste"
)

cursor = conexao.cursor()

# =========================
# INSERT IGNORANDO IDS DUPLICADOS
# =========================

colunas = ", ".join(df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

sql = f"""
INSERT IGNORE INTO vendas ({colunas})
VALUES ({placeholders})
"""

for _, linha in df.iterrows():
    cursor.execute(sql, tuple(linha))

conexao.commit()

print(f"{cursor.rowcount} registros inseridos!")

# =========================
# FECHAR CONEXÃO
# =========================

cursor.close()
conexao.close()