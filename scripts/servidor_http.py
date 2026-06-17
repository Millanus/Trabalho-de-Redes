from http.server import HTTPServer, SimpleHTTPRequestHandler

PORTA = 8000

servidor = HTTPServer(("0.0.0.0", PORTA), SimpleHTTPRequestHandler)

print(f"Servidor HTTP/1.1 rodando na porta {PORTA}")

servidor.serve_forever()
