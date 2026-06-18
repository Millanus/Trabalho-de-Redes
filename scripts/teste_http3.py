import asyncio
import csv
import time
import sys

from aioquic.asyncio.client import connect
from aioquic.h3.connection import H3_ALPN
from aioquic.quic.configuration import QuicConfiguration


CENARIO = sys.argv[1] if len(sys.argv) > 1 else "A"
LATENCIA = sys.argv[2] if len(sys.argv) > 2 else "0"
PERDA = sys.argv[3] if len(sys.argv) > 3 else "0"

ARQUIVO_CSV = "resultados/resultados_http3.csv"


async def medir_conexao():

    configuration = QuicConfiguration(
        alpn_protocols=H3_ALPN,
        is_client=True,
        verify_mode=False
    )

    inicio = time.time()

    async with connect(
        "localhost",
        443,
        configuration=configuration
    ):
        fim = time.time()

    return (fim - inicio) * 1000



async def main():

    resultados = []

    for i in range(10):

        try:
            tempo = await medir_conexao()
            sucesso = 1

        except Exception:
            tempo = 0
            sucesso = 0


        print(f"Teste {i+1}: {tempo:.2f} ms")


        resultados.append([
            "HTTP3",
            CENARIO,
            LATENCIA,
            PERDA,
            i + 1,
            tempo,
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


    print("Resultados salvos em resultados_http3.csv")



asyncio.run(main())
