import pandas as pd
import re

# Lê o arquivo CSV unificado
df = pd.read_csv("data/logs_unificados.csv")

# Listas para armazenar os campos extraídos
ips = []
datas = []
portas = []
eventos = []

# Expressões regulares
regex_ip = r"(?:SRC=)?(\d{1,3}(?:\.\d{1,3}){3})"
regex_data = r"\[([0-9]{2}/[A-Za-z]{3}/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2})"
regex_porta = r"PORT=(\d+)"
regex_evento = r"(Failed password|UFW BLOCK|GET|POST|Invalid user|error|refused|denied)"

# Percorre cada linha do log
for linha in df["conteudo"]:
    # Extrai informações usando regex
    ip = re.search(regex_ip, linha)
    data = re.search(regex_data, linha)
    porta = re.search(regex_porta, linha)
    evento = re.search(regex_evento, linha, re.IGNORECASE)

    ips.append(ip.group(1) if ip else None)
    datas.append(data.group(1) if data else None)
    portas.append(porta.group(1) if porta else None)
    eventos.append(evento.group(1) if evento else "Desconhecido")

# Cria um novo DataFrame com os dados extraídos
df_extraido = pd.DataFrame({
    "arquivo": df["arquivo"],
    "ip_origem": ips,
    "data_hora": datas,
    "porta": portas,
    "evento": eventos,
})

# Exibe as primeiras linhas
print(df_extraido.head(10))

# Salva em um novo arquivo CSV
df_extraido.to_csv("data/logs_processados.csv", index=False)
print("\n✅ Arquivo 'logs_processados.csv' criado com sucesso!")
