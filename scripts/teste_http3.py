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
