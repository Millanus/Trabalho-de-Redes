import csv
import os
import matplotlib.pyplot as plt


arquivo = "resultados/analise_final.csv"

dados = []


with open(arquivo, newline="") as f:
    leitor = csv.DictReader(f)

    for linha in leitor:
        dados.append(linha)


cenarios = ["A", "B", "C", "D"]

http1_media = []
http3_media = []

http1_jitter = []
http3_jitter = []

http1_desvio = []
http3_desvio = []


for c in cenarios:

    for linha in dados:

        if linha["Cenario"] == c and linha["Protocolo"] == "HTTP1":
            http1_media.append(float(linha["Media_ms"]))
            http1_jitter.append(float(linha["Jitter_ms"]))
            http1_desvio.append(float(linha["DesvioPadrao_ms"]))


        if linha["Cenario"] == c and linha["Protocolo"] == "HTTP3":
            http3_media.append(float(linha["Media_ms"]))
            http3_jitter.append(float(linha["Jitter_ms"]))
            http3_desvio.append(float(linha["DesvioPadrao_ms"]))



os.makedirs("resultados/graficos", exist_ok=True)



# Gráfico média

plt.figure(figsize=(8,5))

plt.plot(cenarios, http1_media, marker="o", label="HTTP/1.1")
plt.plot(cenarios, http3_media, marker="o", label="HTTP/3")

plt.xlabel("Cenário")
plt.ylabel("Tempo médio (ms)")
plt.title("Tempo médio de resposta HTTP/1.1 x HTTP/3")
plt.legend()
plt.grid(True)

plt.savefig(
    "resultados/graficos/media_tempo.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# Gráfico jitter

plt.figure(figsize=(8,5))

plt.plot(cenarios, http1_jitter, marker="o", label="HTTP/1.1")
plt.plot(cenarios, http3_jitter, marker="o", label="HTTP/3")

plt.xlabel("Cenário")
plt.ylabel("Jitter (ms)")
plt.title("Jitter HTTP/1.1 x HTTP/3")
plt.legend()
plt.grid(True)

plt.savefig(
    "resultados/graficos/jitter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()



# Gráfico desvio padrão

plt.figure(figsize=(8,5))

plt.plot(cenarios, http1_desvio, marker="o", label="HTTP/1.1")
plt.plot(cenarios, http3_desvio, marker="o", label="HTTP/3")

plt.xlabel("Cenário")
plt.ylabel("Desvio padrão (ms)")
plt.title("Variabilidade dos tempos de resposta")
plt.legend()
plt.grid(True)

plt.savefig(
    "resultados/graficos/desvio_padrao.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Gráficos gerados com sucesso.")
