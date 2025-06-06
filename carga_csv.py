import pandas as pd

# Definir os nomes das colunas do DataFrame com base nas informações disponíveis no arquivo CSV
colunas = [
    "Data", "Hora (UTC)", "Precipitação Total Horária (mm)", "Pressão Atmosférica ao Nível da Estação Horária (mB)",
    "Pressão Atmosférica Máxima na Hora Anterior (mB)", "Pressão Atmosférica Mínima na Hora Anterior (mB)",
    "Radiação Global (KJ/m²)", "Temperatura do Ar - Bulbo Seco Horária (°C)",
    "Temperatura do Ponto de Orvalho (°C)", "Temperatura Máxima na Hora Anterior (°C)",
    "Temperatura Mínima na Hora Anterior (°C)", "Temperatura Orvalho Máxima na Hora Anterior (°C)",
    "Temperatura Orvalho Mínima na Hora Anterior (°C)", "Umidade Relativa Máxima na Hora Anterior (%)",
    "Umidade Relativa Mínima na Hora Anterior (%)", "Umidade Relativa do Ar Horária (%)",
    "Vento - Direção Horária (°)", "Vento - Rajada Máxima (m/s)", "Vento - Velocidade Horária (m/s)"
]

# Carregar o arquivo C em um DataFrame pandas
# Substitua 'curitiba_2015.csv' pelo caminho real do arquivo em sua máquina
try:
    arquivo_csv = "curitiba_2015.csv"
    df = pd.read_csv(arquivo_csv, sep=" ", names=colunas, header=None, skiprows=1, na_values="-9999")

    # Exibir as primeiras linhas do DataFrame
    print(df.head())

except Exception as e:
    print(f"Ocorreu um erro ao carregar o arquivo CSV: {e}")
