import os
import pandas as pd

PASTA_LOGS = "LOGS"
CSV_SAIDA = "logs_unificados.csv"

todos_logs = []

print("🔍 Lendo arquivos da pasta LOGS...\n")

if not os.path.exists(PASTA_LOGS):
    print(f"❌ ERRO: A pasta '{PASTA_LOGS}' não existe.")
    exit()

for arquivo in os.listdir(PASTA_LOGS):
    caminho = os.path.join(PASTA_LOGS, arquivo)
    if not os.path.isfile(caminho) or not arquivo.endswith(".log"):
        continue

    print(f"📄 Lendo arquivo: {arquivo}")

    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                linha = linha.strip()
                if linha:  # Ignora linhas vazias
                    todos_logs.append({"arquivo": arquivo, "conteudo": linha})

    except Exception as e:
        print(f"⚠ Erro ao ler {arquivo}: {e}")

if not todos_logs:
    print("❌ Nenhum arquivo .log encontrado na pasta LOGS.")
    exit()

df = pd.DataFrame(todos_logs)
df.to_csv(CSV_SAIDA, index=False, encoding="utf-8")

print(f"\n✅ Arquivo '{CSV_SAIDA}' criado com sucesso!")
print(f"📁 Total de linhas no CSV: {len(df)}")
