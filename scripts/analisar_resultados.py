import csv
import os
import statistics


PASTA = "resultados/cenarios"

arquivos = [
    ("A", "HTTP1", "http1_A.csv"),
    ("A", "HTTP3", "http3_A.csv"),

    ("B", "HTTP1", "http1_B.csv"),
    ("B", "HTTP3", "http3_B.csv"),

    ("C", "HTTP1", "http1_C.csv"),
    ("C", "HTTP3", "http3_C.csv"),

    ("D", "HTTP1", "http1_D.csv"),
    ("D", "HTTP3", "http3_D.csv"),
]


def calcular_jitter(valores):
    diferencas = []

    for i in range(1, len(valores)):
        diferencas.append(abs(valores[i] - valores[i-1]))

    return statistics.mean(diferencas)


resultados = []


for cenario, protocolo, arquivo in arquivos:

    caminho = os.path.join(PASTA, arquivo)

    tempos = []
    sucessos = []

    with open(caminho, newline="") as f:
        leitor = csv.DictReader(f)

        for linha in leitor:
            tempos.append(float(linha["tempo_ms"]))
            sucessos.append(int(linha["sucesso"]))


    media = statistics.mean(tempos)

    desvio = statistics.stdev(tempos)

    jitter = calcular_jitter(tempos)

    taxa_sucesso = (sum(sucessos) / len(sucessos)) * 100


    resultados.append([
        cenario,
        protocolo,
        media,
        desvio,
        jitter,
        taxa_sucesso
    ])



with open("resultados/analise_final.csv", "w", newline="") as f:

    escritor = csv.writer(f)

    escritor.writerow([
        "Cenario",
        "Protocolo",
        "Media_ms",
        "DesvioPadrao_ms",
        "Jitter_ms",
        "TaxaSucesso_pct"
    ])

    escritor.writerows(resultados)


print("Análise concluída.")
print("Arquivo gerado: resultados/analise_final.csv")
