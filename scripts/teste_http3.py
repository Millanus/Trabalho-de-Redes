import asyncio
import time

from aioquic.asyncio.client import connect
from aioquic.h3.connection import H3_ALPN
from aioquic.quic.configuration import QuicConfiguration

async def main():
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
    ) as client:

        fim = time.time()

        tempo = (fim - inicio) * 1000

        print(f"Conexão HTTP/3 estabelecida em {tempo:.2f} ms")

asyncio.run(main())
