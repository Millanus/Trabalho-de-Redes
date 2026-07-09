<<<<<<< HEAD
# Trabalho de Redes de Computadores

> **Análise Comparativa entre HTTP/1.1 e HTTP/3 em Diferentes Condições de Rede**

**Professor:** *(Adicionar link do trabalho aqui)*

## Integrantes

- **Guilherme Dornelles Guarienti Millani** (2510200473) — Líder
- **Iago Leão Silveira de Souza** (2010200689)

---

# 1. Introdução

O protocolo **HTTP (Hypertext Transfer Protocol)** é a base da World Wide Web, permitindo a comunicação entre clientes e servidores.

Com o crescimento das aplicações web, tornou-se necessário evoluir os protocolos para oferecer maior desempenho e segurança.

O **HTTP/1.1** apresenta limitações importantes, como:

- Head-of-Line Blocking;
- Overhead de conexões;
- Dependência do TCP.

Já o **HTTP/3**, baseado no protocolo **QUIC**, busca reduzir esses problemas oferecendo melhor desempenho, principalmente em redes com perda de pacotes e alta latência.

Este trabalho procura responder à seguinte questão:

> **Em quais condições de rede o HTTP/3 realmente apresenta vantagens em relação ao HTTP/1.1?**

---

# 2. Objetivo

Comparar os protocolos **HTTP/1.1** e **HTTP/3**, medindo:

- RTT (Round Trip Time)
- Page Load Time
- Jitter
- Estabilidade da conexão

em diferentes cenários simulados de rede.

---

# 3. Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Docker | Ambientes isolados |
| tc (netem) | Simulação de latência e perda |
| Python | Automação dos testes |
| requests | Cliente HTTP/1.1 |
| aioquic | Cliente HTTP/3 |
| Caddy Server | Servidor HTTP/3 |
| Wireshark | Captura de tráfego |
| Mininet *(planejado)* | Emulação de redes |

---

# 4. Desenvolvimento

## 4.1 Cenário Simulado

Foi utilizado um ambiente inspirado em uma rede hospitalar contendo:

- 50–100 usuários simultâneos;
- acesso a imagens médicas;
- prontuário eletrônico via navegador;
- conexão local com acesso externo.

---

## 4.2 Variáveis do Experimento

### Protocolos

- HTTP/1.1 (TCP + TLS)
- HTTP/3 (QUIC/UDP)

### Condições de rede

- Latência
- Perda de pacotes

### Quantidade de requisições

- 10
- 50
- 100

---

## 4.3 Parâmetros

| Parâmetro | Valores |
|-----------|---------|
| Latência | 0, 50, 100, 200 ms |
| Perda | 0%, 1%, 5% |
| Repetições | 10 |
| Método | HTTP GET |

---

## 4.4 Cenários

| Cenário | Latência | Perda | Objetivo |
|----------|----------|--------|----------|
| A | 0 ms | 0% | Baseline |
| B | 50 ms | 0% | Rede hospitalar normal |
| C | 100 ms | 1% | Horário de pico |
| D | 200 ms | 5% | Rede degradada |

---

## 4.5 Métricas Avaliadas

- RTT
- Tempo de carregamento
- Jitter
- Taxa de sucesso

---

# 5. Infraestrutura

- Docker
- Caddy Server
- Python 3
- requests
- aioquic
- tc (netem)
- Wireshark
- Mininet (planejado)

---

# 6. Configuração da Rede

## Cenário B

```bash
sudo tc qdisc add dev lo root netem delay 50ms
```

## Cenário C

```bash
sudo tc qdisc add dev lo root netem delay 100ms loss 1%
```

## Cenário D

```bash
sudo tc qdisc add dev lo root netem delay 200ms loss 5%
```

Remover configuração:

```bash
sudo tc qdisc del dev lo root
```

---

# 7. Coleta de Dados

Foram utilizados dois clientes independentes:

- Cliente HTTP/1.1
- Cliente HTTP/3

Cada cenário executou **10 requisições** por protocolo.

Os resultados foram armazenados em arquivos CSV contendo:

- protocolo
- cenário
- latência
- perda
- número da execução
- tempo (ms)
- sucesso

---

# 8. Evidências dos Testes

## Inicialização

- Servidor HTTP/1.1 (porta 8000)
- Servidor HTTP/3 via Docker (porta 443)

### Figuras

- Figura 1 — Servidor HTTP/1.1
- Figura 2 — Servidor HTTP/3 (Docker)

---

## Cenário A

Execução dos clientes HTTP/1.1 e HTTP/3.

- Figura 3
- Figura 4

---

## Teste com perda de pacotes

100 ms de atraso + 1% de perda.

Figura 5.

---

## Validação do HTTP/3

- Caddy com QUIC
- Porta UDP 443
- Cliente aioquic

Figuras:

- Figura 6
- Figura 7
- Figura 8

---

## Captura no Wireshark

HTTP/1.1

- TCP
- Porta 8000

HTTP/3

- UDP
- Porta 443

Figuras:

- Figura 9
- Figura 10

---

# 9. Resultados

| Cenário | Protocolo | Média (ms) | Desvio | Jitter | Sucesso |
|---------|-----------|-----------:|--------:|--------:|---------:|
| A | HTTP/1.1 | 7.41 | 10.78 | 6.73 | 100% |
| A | HTTP/3 | 32.97 | 42.88 | 19.84 | 100% |
| B | HTTP/1.1 | 208.84 | 3.69 | 4.14 | 100% |
| B | HTTP/3 | 114.32 | 4.50 | 3.96 | 100% |
| C | HTTP/1.1 | 408.51 | 4.86 | 4.80 | 100% |
| C | HTTP/3 | 239.50 | 62.68 | 51.10 | 100% |
| D | HTTP/1.1 | 861.10 | 159.06 | 114.17 | 100% |
| D | HTTP/3 | 459.90 | 125.83 | 91.19 | 100% |

---

## Gráficos

- Gráfico 1 — Tempo médio
- Gráfico 2 — Jitter
- Gráfico 3 — Desvio padrão

---

# 10. Discussão

## HTTP/1.1 × HTTP/3

No cenário sem degradação, o HTTP/1.1 apresentou menor tempo médio.

À medida que aumentaram a latência e a perda de pacotes, o HTTP/3 passou a apresentar desempenho superior.

### Comparação

| Cenário | HTTP/1.1 | HTTP/3 |
|----------|----------:|--------:|
| B | 208.84 ms | 114.32 ms |
| C | 408.51 ms | 239.50 ms |
| D | 861.10 ms | 459.90 ms |

---

## Motivos

### HTTP/1.1

- TCP
- Three-way Handshake
- TLS separado
- Retransmissões

### HTTP/3

- QUIC
- UDP
- TLS integrado
- Melhor tratamento para perdas

---

# 11. Conclusão

Os experimentos mostraram que:

- HTTP/1.1 é mais rápido apenas em ambiente ideal;
- HTTP/3 apresenta desempenho significativamente superior em redes degradadas;
- no cenário mais severo houve aproximadamente **46% de redução** no tempo médio de resposta.

No contexto hospitalar simulado, essa diferença representa menor tempo de acesso a imagens médicas e maior agilidade na tomada de decisão clínica.

Embora os testes tenham sido realizados em ambiente controlado, os resultados reforçam que o HTTP/3 representa uma evolução importante em relação ao HTTP/1.1, principalmente devido às características do protocolo QUIC.

---

# Trabalhos Futuros

- Utilização do Mininet
- Simulação com múltiplos clientes
- Arquivos DICOM reais
- Maior volume de tráfego
- Ambientes distribuídos
- Comparação entre diferentes servidores HTTP/3

---

# Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.
