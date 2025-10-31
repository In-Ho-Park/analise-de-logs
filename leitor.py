import os
import pandas as pd

# Caminho da pasta onde estão os logs
log_dir = "."  # ou "data/logs" se mover os arquivos pra lá

# Lista para armazenar os dados
logs_data = []

# Percorre todos os arquivos da pasta
for filename in os.listdir(log_dir):
    if filename.endswith(".txt") or filename.endswith(".log"):
        file_path = os.path.join(log_dir, filename)
        print(f"Lendo arquivo: {filename}")

        # Abre o arquivo e lê linha por linha
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:  # ignora linhas vazias
                    logs_data.append({
                        "arquivo": filename,
                        "conteudo": line
                    })

# Converte para um DataFrame
df_logs = pd.DataFrame(logs_data)

# Mostra as primeiras linhas
print("\nPrimeiras linhas lidas:")
print(df_logs.head())

# Salva tudo em um CSV
df_logs.to_csv("logs_unificados.csv", index=False)
print("\n✅ Arquivo 'logs_unificados.csv' criado com sucesso!")
