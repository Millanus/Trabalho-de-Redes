import requests
import time
import csv
import sys

URL = "http://localhost:8000"
NUM_TESTES = 10

CENARIO = sys.argv[1] if len(sys.argv) > 1 else "A"
LATENCIA = sys.argv[2] if len(sys.argv) > 2 else "0"
PERDA = sys.argv[3] if len(sys.argv) > 3 else "0"

ARQUIVO_CSV = "resultados/resultados_http.csv"

resultados = []

for i in range(NUM_TESTES):

    inicio = time.time()

    try:
        resposta = requests.get(URL)

        fim = time.time()

        tempo_resposta = (fim - inicio) * 1000

        sucesso = 1

    except Exception:
        fim = time.time()

        tempo_resposta = (fim - inicio) * 1000

        sucesso = 0


    print(f"Teste {i+1}: {tempo_resposta:.2f} ms")

    resultados.append([
        "HTTP1",
        CENARIO,
        LATENCIA,
        PERDA,
        i + 1,
        tempo_resposta,
        sucesso
    ])


with open(ARQUIVO_CSV, "w", newline="") as arquivo:

    writer = csv.writer(arquivo)

    writer.writerow([
        "protocolo",
        "cenario",
        "latencia_ms",
        "perda_pct",
        "execucao",
        "tempo_ms",
        "sucesso"
    ])

    writer.writerows(resultados)


print(f"Resultados salvos em {ARQUIVO_CSV}")
