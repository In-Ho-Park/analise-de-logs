import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
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

# ============================================================
#  MACHINE LEARNING 1 — Isolation Forest
# ============================================================

modelo_if = IsolationForest(contamination=0.15, random_state=42)
ip_counts["anomalia_if"] = modelo_if.fit_predict(ip_counts[["qtd_eventos"]])

suspeitos_if = ip_counts[ip_counts["anomalia_if"] == -1]

print("\n🚨 IPs suspeitos detectados (Isolation Forest):")
print(suspeitos_if)

# ============================================================
#  MACHINE LEARNING 2 — Local Outlier Factor (LOF)
# ============================================================

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.15)
resultado_lof = lof.fit_predict(ip_counts[["qtd_eventos"]])

ip_counts["anomalia_lof"] = resultado_lof

suspeitos_lof = ip_counts[ip_counts["anomalia_lof"] == -1]

print("\n🔥 IPs suspeitos detectados (Local Outlier Factor):")
print(suspeitos_lof)

# ============================================================
#  Gráfico — IPs e suspeitos (Isolation Forest)
# ============================================================

plt.figure(figsize=(12, 6))
plt.bar(ip_counts["ip_origem"], ip_counts["qtd_eventos"], color="gray")
plt.bar(suspeitos_if["ip_origem"], suspeitos_if["qtd_eventos"], color="red")
plt.xticks(rotation=45, ha="right")
plt.title("Atividade de IPs (vermelho = suspeito — Isolation Forest)")
plt.xlabel("IP de origem")
plt.ylabel("Quantidade de eventos")
plt.tight_layout()
plt.show()

# ============================================================
#  Exporta os resultados
# ============================================================

suspeitos_if.to_csv("ips_suspeitos_isolation_forest.csv", index=False)
suspeitos_lof.to_csv("ips_suspeitos_lof.csv", index=False)

print("\n Arquivos gerados:")
print(" - ips_suspeitos_isolation_forest.csv")
print(" - ips_suspeitos_lof.csv")
