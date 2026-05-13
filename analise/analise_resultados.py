import csv
import statistics
import matplotlib.pyplot as plt

tempos = []

with open('../resultados/resultados_http.csv', newline='') as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        tempos.append(float(linha['TempoResposta_ms']))

media = statistics.mean(tempos)
minimo = min(tempos)
maximo = max(tempos)

print(f"Média: {media:.2f} ms")
print(f"Mínimo: {minimo:.2f} ms")
print(f"Máximo: {maximo:.2f} ms")

plt.plot(tempos, marker='o')
plt.title('Tempo de Resposta HTTP')
plt.xlabel('Teste')
plt.ylabel('Tempo (ms)')
plt.grid(True)

plt.savefig('../resultados/grafico_http.png')

print("Gráfico salvo em grafico_http.png")
