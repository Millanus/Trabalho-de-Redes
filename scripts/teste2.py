import requests
import time

URL = "http://localhost:8000"

def testar(nome):
    tempos = []

    for i in range(10):
        inicio = time.time()
        requests.get(URL)
        fim = time.time()

        delta = (fim - inicio) * 1000
        tempos.append(delta)

        print(f"{nome} teste {i+1}: {delta:.2f} ms")

    media = sum(tempos) / len(tempos)
    print(f"\n{nome} média: {media:.2f} ms\n")


testar("HTTP/1.1")
