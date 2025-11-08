import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# === Lê o CSV processado ===
df = pd.read_csv("logs_processados.csv")

print("\nPrimeiras linhas do arquivo processado:")
print(df.head())

# Remove linhas sem IP
df = df.dropna(subset=["ip_origem"])

# === Conta quantos eventos cada IP fez ===
ip_counts = df["ip_origem"].value_counts().reset_index()
ip_counts.columns = ["ip_origem", "qtd_eventos"]

# === Aplica Isolation Forest para detectar IPs fora do padrão ===
modelo = IsolationForest(contamination=0.15, random_state=42)
ip_counts["anomalia"] = modelo.fit_predict(ip_counts[["qtd_eventos"]])

# -1 = suspeito, 1 = normal
suspeitos = ip_counts[ip_counts["anomalia"] == -1]
normais = ip_counts[ip_counts["anomalia"] == 1]

print("\n🚨 IPs suspeitos detectados:")
print(suspeitos)

# === Gera gráfico dos IPs mais ativos ===
plt.figure(figsize=(10, 5))
plt.bar(ip_counts["ip_origem"], ip_counts["qtd_eventos"], color="gray")
plt.bar(suspeitos["ip_origem"], suspeitos["qtd_eventos"], color="red")
plt.xticks(rotation=45, ha="right")
plt.title("Atividade de IPs (vermelho = suspeito)")
plt.xlabel("IP de origem")
plt.ylabel("Quantidade de eventos")
plt.tight_layout()
plt.show()

# === Exporta IPs suspeitos ===
suspeitos.to_csv("ips_suspeitos.csv", index=False)
print("\n Lista salva em 'ips_suspeitos.csv'")
