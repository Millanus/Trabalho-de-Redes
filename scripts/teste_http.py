import requests
import time
import csv

URL = "http://localhost:8000"
NUM_TESTES = 10

resultados = []

for i in range(NUM_TESTES):
    inicio = time.time()

    resposta = requests.get(URL)

    fim = time.time()

    tempo_resposta = (fim - inicio) * 1000  # ms

    print(f"Teste {i+1}: {tempo_resposta:.2f} ms")

    resultados.append([i + 1, tempo_resposta])

with open("resultados/resultados_http.csv", "w", newline="") as arquivo:
    writer = csv.writer(arquivo)

    writer.writerow(["Teste", "TempoResposta_ms"])

    writer.writerows(resultados)

print("Resultados salvos em resultados_http.csv")
