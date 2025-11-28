import pandas as pd
import re

df = pd.read_csv("logs_unificados.csv")

ips = []
datas = []
portas = []
eventos = []

# REGEX MELHORADOS
regex_ip = r"(?:SRC=|from )(\d{1,3}(?:\.\d{1,3}){3})|^(\d{1,3}(?:\.\d{1,3}){3})"
regex_data_syslog = r"([A-Za-z]{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})"
regex_data_apache = r"\[([0-9]{2}/[A-Za-z]{3}/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2})"
regex_porta = r"(?:DPT|SPT|PORT)=(\d+)"

regex_evento = r"(Failed password|Accepted password|invalid user|UFW BLOCK|UFW ALLOW|IPTABLES_DROP|Connection closed|GET\s+\S+|POST\s+\S+)"


for linha in df["conteudo"]:

    # IP
    ip_match = re.search(regex_ip, linha)
    if ip_match:
        ip = ip_match.group(1) or ip_match.group(2)
    else:
        ip = None

    # DATA (syslog)
    data_match1 = re.search(regex_data_syslog, linha)

    # DATA (apache)
    data_match2 = re.search(regex_data_apache, linha)

    data = data_match1.group(1) if data_match1 else (
           data_match2.group(1) if data_match2 else None)

    # PORTA
    porta_match = re.search(regex_porta, linha)
    porta = porta_match.group(1) if porta_match else None

    # EVENTO
    evento_match = re.search(regex_evento, linha, re.IGNORECASE)
    evento = evento_match.group(1) if evento_match else "Desconhecido"

    ips.append(ip)
    datas.append(data)
    portas.append(porta)
    eventos.append(evento)

df_extraido = pd.DataFrame({
    "arquivo": df["arquivo"],
    "ip_origem": ips,
    "data_hora": datas,
    "porta": portas,
    "evento": eventos,
})

print(df_extraido.head(20))

df_extraido.to_csv("logs_processados.csv", index=False)
print("\n Arquivo 'logs_processados.csv' criado com sucesso!")
