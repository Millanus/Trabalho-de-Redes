# Comparação de Desempenho entre HTTP/1.1 e HTTP/3 em Ambiente Hospitalar Simulado

Trabalho da disciplina de Redes de Computadores, propondo uma análise comparativa entre os protocolos **HTTP/1.1** e **HTTP/3**, com foco em métricas de latência, jitter e estabilidade de conexão em cenários inspirados em uma rede hospitalar.

## Integrantes

- Guilherme Dornelles Guarienti Millani (2510200473) – Líder
- Iago Leão Silveira de Souza (2010200689)

---

## 1. Introdução

O protocolo HTTP (Hypertext Transfer Protocol) é a base da World Wide Web, permitindo a comunicação entre clientes e servidores. Com o crescimento das aplicações web, que passaram a exigir maior velocidade e segurança, tornou-se necessário evoluir os protocolos de comunicação para suportar conexões mais eficientes e criptografadas.

O HTTP/1.1 apresenta limitações de desempenho, como o problema de bloqueio de início de linha (*Head-of-Line Blocking*) e overhead de conexão. Embora o HTTP/3 traga melhorias de desempenho em cenários com perda de pacotes por meio do uso do protocolo QUIC, ainda há relativamente poucos estudos comparativos diretos entre HTTP/3 e HTTP/1.1 em cenários variados de rede, o que dificulta uma análise mais clara sobre quando sua adoção é mais vantajosa.

## 2. Proposta

Este trabalho propõe uma análise comparativa entre os protocolos HTTP/1.1 e HTTP/3. A proposta é medir métricas como latência (RTT) e tempo de carregamento de páginas (*Page Load Time*) em um ambiente controlado, simulando diferentes condições de rede, como atraso e perda de pacotes, para avaliar os ganhos de desempenho do HTTP/3.

### Tecnologias utilizadas

- **Docker** — criação de ambientes isolados e reprodutíveis
- **tc (Traffic Control)** — simulação de diferentes condições de rede
- **Scripts em Python** — coleta de dados, utilizando bibliotecas compatíveis com QUIC e a biblioteca padrão `socket`/`requests` para conexões HTTP/1.1
- **Wireshark** — análise detalhada do tráfego de rede
- **Mininet** — emulação de topologias de rede controladas (uso planejado)

---

## 3. Desenvolvimento

O trabalho adota um cenário simulado inspirado em ambientes hospitalares que utilizam sistemas de transferência e visualização de imagens médicas (como exames de tomografia, ressonância magnética e radiografias) por meio de aplicações web. Esse tipo de sistema é particularmente sensível a variações de latência e estabilidade de rede, uma vez que a transmissão de imagens médicas pode impactar diretamente a tomada de decisão clínica.

### 3.1 Contexto do ambiente hospitalar simulado

O ambiente modelado representa uma rede hospitalar de médio porte, contendo:

- Aproximadamente 50 a 100 usuários simultâneos (médicos, técnicos e sistemas automatizados)
- Múltiplos dispositivos acessando imagens médicas em servidores centrais
- Tráfego predominantemente composto por requisições de arquivos de imagem (JPEG/PNG/DICOM simplificado) e carregamento de páginas de prontuário eletrônico
- Uso de rede local com conexão externa intermitente (simulando dependência de infraestrutura mista)

### 3.2 Fatores do experimento

- **Protocolo de aplicação:** HTTP/1.1 (baseado em TCP, com TLS 1.3) e HTTP/3 (baseado em QUIC/UDP)
- **Condição de rede:** latência artificial (introduzida via `tc netem`) e perda de pacotes
- **Carga de requisições:** número fixo de requisições por teste (10, 50 e 100 requisições planejadas)

### 3.3 Parâmetros de configuração

- **Latência:** 0 ms, 50 ms, 100 ms e 200 ms
- **Perda de pacotes** (cenário futuro): 0%, 1% e 5%
- **Número de execuções por cenário:** 10 repetições
- **Tipo de requisição:** HTTP GET para arquivos de imagem e páginas web simuladas

### 3.4 Cenários experimentais

| Cenário | Descrição | Latência | Perda | Objetivo |
|---|---|---|---|---|
| **A** | Rede ideal (baseline) | 0 ms | 0% | Estabelecer referência de desempenho |
| **B** | Rede hospitalar estável | 50 ms | 0% | Simular operação interna normal |
| **C** | Rede hospitalar congestionada | 100 ms | 1% | Simular horário de pico e sobrecarga |
| **D** | Rede degradada (em estudo) | 200 ms | 5% | Simular falhas de infraestrutura ou link externo instável |

### 3.5 Métricas de avaliação

- RTT (Round Trip Time)
- Tempo de carregamento de requisições (Page Load Time)
- Variação de tempo entre requisições (jitter)
- Estabilidade de conexão sob perda de pacotes

### 3.6 Infraestrutura tecnológica

- **Docker** — criação de ambientes isolados para servidores HTTP/1.1 e HTTP/3
- **Caddy Server** — implementação do HTTP/3 com suporte nativo a QUIC
- **Python 3** — automação dos testes e coleta de métricas
- **requests** (Python) — execução de requisições HTTP/1.1
- **aioquic** (Python) — execução de requisições HTTP/3 sobre QUIC
- **tc (Traffic Control / netem)** — simulação de latência e perda de pacotes
- **Wireshark** — análise de tráfego de rede (TCP e UDP/QUIC)
- **Mininet** (planejado) — emulação de topologias de rede hospitalar

### 3.7 Configuração das condições de rede

Para simular diferentes condições de rede, foi utilizada a ferramenta `tc netem`, disponível no Linux, permitindo introduzir artificialmente latência e perda de pacotes em uma interface de rede. Os experimentos foram realizados sobre a interface de loopback (`lo`).

**Cenário B (50 ms de latência):**
```bash
sudo tc qdisc add dev lo root netem delay 50ms
```

**Cenário C (100 ms de latência e 1% de perda):**
```bash
sudo tc qdisc add dev lo root netem delay 100ms loss 1%
```

**Cenário D (200 ms de latência e 5% de perda):**
```bash
sudo tc qdisc add dev lo root netem delay 200ms loss 5%
```

Após cada conjunto de testes, as configurações eram removidas:
```bash
sudo tc qdisc del dev lo root
```

A correta aplicação das regras foi validada pela observação do aumento dos tempos de resposta medidos pelos clientes HTTP/1.1 e HTTP/3.

### 3.8 Coleta e armazenamento dos dados

Foram desenvolvidos dois scripts independentes: um para o protocolo HTTP/1.1 (usando a biblioteca `requests`) e outro para HTTP/3 (usando a biblioteca `aioquic`, conectando ao servidor Caddy). Para cada cenário experimental foram executadas dez requisições consecutivas por protocolo, com os resultados armazenados em arquivos CSV.

**Campos registrados em cada execução:**

| Campo | Descrição |
|---|---|
| `protocolo` | Protocolo utilizado (HTTP/1.1 ou HTTP/3) |
| `cenario` | Cenário experimental avaliado |
| `latencia_ms` | Latência configurada via `tc netem` |
| `perda_pct` | Percentual de perda de pacotes configurado |
| `execucao` | Número da execução |
| `tempo_ms` | Tempo total observado para a requisição |
| `sucesso` | Indicador de sucesso (1 = sucesso, 0 = falha) |

---

## 4. Evidências de Execução dos Testes

> As imagens/prints de terminal referenciadas abaixo (Figuras 1 a 10) fazem parte do relatório completo do trabalho.

### 4.1 Inicialização dos servidores HTTP/1.1 e HTTP/3

O servidor HTTP/1.1 foi inicializado localmente na porta 8000 utilizando o módulo `http.server` do Python, enquanto o servidor HTTP/3 foi inicializado via Docker, utilizando o Caddy Server com suporte nativo a QUIC na porta 443

<img width="1207" height="457" alt="Figura 1" src="https://github.com/user-attachments/assets/ae230b31-54ef-4770-aed3-46d6919e910e" />
Figura 1 — Inicialização do servidor HTTP/1.1 (porta 8000).


<img width="902" height="609" alt="FIGURA 2" src="https://github.com/user-attachments/assets/f57e66a8-3ed0-4e96-a6c3-06eaa1a33cb2" />
- Figura 2 — Inicialização do ambiente HTTP/3 via Docker Compose (servidor Caddy)

### 4.2 Testes básicos de latência (Cenário A — Baseline)

Os testes iniciais em ambiente local sem degradação de rede (Cenário A) resultaram em tempos médios de aproximadamente 5 a 9 ms para o HTTP/1.1.


<img width="905" height="373" alt="FIGURA 3" src="https://github.com/user-attachments/assets/b4cc17a2-5ef6-47f9-81a4-dcf3dfbed8fa" />
      - Figura 3 — Execução do cliente HTTP/1.1 e coleta das métricas (Cenário A)


<img width="1402" height="347" alt="FIGURA 4" src="https://github.com/user-attachments/assets/b3fd68de-037b-49f2-9208-3a740afd57e0" />
     - Figura 4 — Execução do cliente HTTP/3 (aioquic) e coleta das métricas (Cenário A)

### 4.3 Teste preliminar com perda de pacotes

Foi realizado um teste preliminar utilizando HTTP/1.1 em ambiente controlado, com degradação artificial de rede (100 ms de latência e 1% de perda de pacotes). Os resultados indicaram aumento significativo no tempo de resposta e maior variação entre requisições consecutivas, com alguns casos ultrapassando 1 segundo (chegando a ~5 segundos), comportamento associado ao impacto de retransmissões no TCP sob perda de pacotes.



<img width="1283" height="702" alt="FIGURA 5" src="https://github.com/user-attachments/assets/9a7a275b-7dfa-4e7e-b12e-4a10d506857b" />
- Figura 5 — Teste HTTP/1.1 com 100 ms de latência e 1% de perda de pacotes (tc netem)

### 4.4 Validação inicial do ambiente HTTP/3

Foi realizada a configuração inicial do ambiente HTTP/3 utilizando o servidor Caddy com suporte nativo a QUIC. Os testes preliminares confirmaram a ativação do listener HTTP/3, o suporte simultâneo aos protocolos HTTP/1.1, HTTP/2 e HTTP/3, e a exposição da porta UDP 443 necessária para a comunicação QUIC. O cliente experimental em Python (aioquic) confirmou o estabelecimento de uma conexão HTTP/3 em aproximadamente 203 ms na validação inicial.



<img width="1284" height="359" alt="FIGURA 6" src="https://github.com/user-attachments/assets/e50946de-8d8c-4fa3-a9e3-efa504382f4d" />
- Figura 6 — Container Caddy em execução, com a porta 443 exposta em TCP e UDP


<img width="1125" height="731" alt="FIGURA 7" src="https://github.com/user-attachments/assets/c165c823-2e7e-4d56-96fe-a0962788441d" />
- Figura 7 — Logs do servidor Caddy demonstrando a habilitação do HTTP/3 (QUIC) e suporte aos protocolos h1, h2 e h3


<img width="1530" height="195" alt="FIGURA 8" src="https://github.com/user-attachments/assets/8e3f221f-3403-48b3-a6a8-05aeb0b63399" />
- Figura 8 — Conexão HTTP/3 estabelecida com sucesso pelo cliente experimental em Python (aioquic)

Durante o desenvolvimento, também foram registradas falhas pontuais de conexão (`ConnectionError`) no cliente HTTP/3, posteriormente contornadas, o que evidencia a maior complexidade de implementação do QUIC em comparação ao modelo cliente-servidor tradicional do HTTP/1.1.

### 4.5 Captura de tráfego com Wireshark

O tráfego HTTP/1.1 foi capturado na interface de loopback, filtrado pela porta TCP 8000, confirmando o uso do protocolo TCP com o *three-way handshake* característico. Já o tráfego HTTP/3 foi observado na porta UDP 443, utilizada pelo protocolo QUIC.



<img width="789" height="611" alt="FIGURA 9" src="https://github.com/user-attachments/assets/847f7e7e-006e-4246-9960-a2572288428a" />
- Figura 9 — Captura de tráfego HTTP/1.1 (TCP, porta 8000)

<img width="788" height="615" alt="FIGURA 10" src="https://github.com/user-attachments/assets/d4695c58-f8bb-4b23-a7d5-617faee3a92a" />
- Figura 10 — Captura de tráfego HTTP/3 (QUIC sobre UDP, porta 443)

---

## 5. Resultados Obtidos

Os resultados consolidados dos experimentos são apresentados na tabela abaixo, com as métricas de tempo médio de resposta, desvio padrão, jitter e taxa de sucesso para cada protocolo em todos os cenários avaliados.

**Tabela 1 — Resultados experimentais**

| Cenário | Protocolo | Média (ms) | Desvio Padrão (ms) | Jitter (ms) | Sucesso (%) |
|---|---|---|---|---|---|
| A | HTTP/1.1 | 7,41 | 10,78 | 6,73 | 100 |
| A | HTTP/3 | 32,97 | 42,88 | 19,84 | 100 |
| B | HTTP/1.1 | 208,84 | 3,69 | 4,14 | 100 |
| B | HTTP/3 | 114,32 | 4,50 | 3,96 | 100 |
| C | HTTP/1.1 | 408,51 | 4,86 | 4,80 | 100 |
| C | HTTP/3 | 239,50 | 62,68 | 51,10 | 100 |
| D | HTTP/1.1 | 861,10 | 159,06 | 114,17 | 100 |
| D | HTTP/3 | 459,90 | 125,83 | 91,19 | 100 |

Observa-se que ambos os protocolos obtiveram taxa de sucesso de 100% em todos os cenários. Entretanto, à medida que a latência e a perda de pacotes aumentaram, o HTTP/3 apresentou tempos médios inferiores aos observados para o HTTP/1.1, especialmente nos cenários C e D.

O aumento progressivo da latência e da perda de pacotes impactou negativamente ambos os protocolos. Entretanto, o HTTP/3 apresentou crescimento menos acentuado do tempo médio de resposta em comparação ao HTTP/1.1. Nos cenários mais degradados (C e D), o protocolo HTTP/3 manteve desempenho superior, indicando maior robustez diante de condições adversas de rede. A taxa de sucesso permaneceu em 100% em todos os experimentos, evidenciando estabilidade operacional em ambos os protocolos.


<img width="1037" height="667" alt="GRAFICO 1" src="https://github.com/user-attachments/assets/20516069-d661-48bc-bb4e-e6b7445c8c34" />
> Gráfico 1 — Tempo médio de resposta por cenário: HTTP/1.1 x HTTP/3


<img width="1055" height="656" alt="GRAFICO 2" src="https://github.com/user-attachments/assets/e7b93751-7af8-4cb0-86b4-cbd091e4e501" />
> Gráfico 2 — Jitter por cenário: HTTP/1.1 x HTTP/3


<img width="975" height="653" alt="GRAFICO 3" src="https://github.com/user-attachments/assets/d86aeab9-a062-447b-a074-2d16e7492460" />
> Gráfico 3 — Desvio padrão (variabilidade) dos tempos de resposta por cenário

---

## 6. Discussão

### 6.1 Comparação entre HTTP/1.1 e HTTP/3

Os resultados obtidos demonstram diferenças significativas de desempenho entre os protocolos HTTP/1.1 e HTTP/3 nos cenários analisados.

No **Cenário A** (0 ms de atraso e 0% de perda), o HTTP/1.1 apresentou menor tempo médio de resposta (7,41 ms) em comparação ao HTTP/3 (32,97 ms). Esse resultado pode ser explicado pelo fato de que, em um ambiente local sem degradação da rede, o custo adicional do estabelecimento da conexão QUIC e das bibliotecas utilizadas para implementação do HTTP/3 torna-se mais perceptível.

Entretanto, à medida que as condições da rede se tornam mais adversas, observa-se uma mudança significativa no comportamento dos protocolos:

- **Cenário B** (50 ms de atraso, 0% de perda): HTTP/3 com 114,32 ms, contra 208,84 ms do HTTP/1.1
- **Cenário C** (100 ms de atraso, 1% de perda): HTTP/3 com 239,50 ms, contra 408,51 ms do HTTP/1.1
- **Cenário D** (200 ms de atraso, 5% de perda): HTTP/3 com 459,90 ms, contra 861,10 ms do HTTP/1.1

Dessa forma, verifica-se que o HTTP/3 apresentou desempenho progressivamente superior conforme aumentaram a latência e a perda de pacotes da rede.

### 6.2 Explicação das diferenças observadas

As diferenças observadas decorrem principalmente das características dos protocolos de transporte utilizados por cada versão do HTTP.

O HTTP/1.1 utiliza o protocolo TCP, que exige o estabelecimento de conexão por meio do *three-way handshake* e, em conexões seguras, também o handshake do TLS. Quando ocorre perda de pacotes, o TCP tende a retransmitir segmentos e pode reduzir sua janela de congestionamento, aumentando o tempo necessário para a entrega dos dados.

Já o HTTP/3 utiliza o protocolo QUIC, implementado sobre UDP. O QUIC integra mecanismos de transporte e segurança em um único protocolo, reduzindo o número de etapas necessárias para estabelecer a comunicação, além de ter sido projetado para lidar melhor com perdas de pacotes e redes de alta latência.

Os resultados experimentais confirmam essa característica: à medida que a latência e a perda aumentaram, o ganho de desempenho do HTTP/3 tornou-se mais evidente.

### 6.3 Relação dos resultados com TCP e QUIC

No HTTP/1.1, a dependência do TCP faz com que atrasos na transmissão e retransmissões tenham impacto direto sobre toda a conexão — comportamento particularmente perceptível nos Cenários C e D. No HTTP/3, o uso do QUIC permitiu maior resiliência diante das mesmas condições de rede; embora também tenham ocorrido aumentos nos tempos médios, esses aumentos foram significativamente menores.

A análise do tráfego capturado no Wireshark confirmou ainda a utilização de TCP na comunicação HTTP/1.1 e de UDP na porta 443 para a comunicação baseada em QUIC utilizada pelo HTTP/3, corroborando a arquitetura prevista para cada protocolo e alinhando os resultados obtidos com o comportamento descrito na literatura especializada sobre HTTP/3 e QUIC.

---

## 7. Conclusão

O objetivo deste trabalho foi comparar o desempenho dos protocolos HTTP/1.1 e HTTP/3 em diferentes condições de rede, analisando o impacto da latência e da perda de pacotes sobre o tempo de resposta das aplicações.

Foram implementados ambientes experimentais utilizando um servidor HTTP/1.1 convencional e um servidor HTTP/3 baseado em QUIC, com testes em quatro cenários distintos, variando os níveis de atraso e perda de pacotes por meio da ferramenta `tc netem`.

Os resultados mostraram que o HTTP/1.1 apresentou melhor desempenho apenas no cenário sem degradação da rede, onde o custo adicional do QUIC se tornou mais perceptível. Nos cenários com aumento de latência e perda de pacotes, o HTTP/3 apresentou desempenho significativamente superior. No cenário mais severo (200 ms de atraso e 5% de perda), o tempo médio do HTTP/3 foi aproximadamente **46% menor** que o observado para o HTTP/1.1.

Esses resultados têm implicações diretas para o contexto hospitalar simulado neste trabalho. Em um ambiente com 50 a 100 usuários simultâneos acessando imagens médicas de alta resolução (como tomografias e ressonâncias), a superioridade do HTTP/3 nos Cenários C e D — que simulam, respectivamente, o horário de pico (100 ms, 1% de perda) e falhas de infraestrutura (200 ms, 5% de perda) — é especialmente relevante. Nesses cenários, a redução de aproximadamente **41% e 46%** no tempo de resposta representa não apenas ganho de desempenho técnico, mas potencial impacto na agilidade da tomada de decisão clínica, onde atrasos na visualização de imagens diagnósticas podem comprometer o atendimento ao paciente.

### Limitações do estudo

- Experimentos realizados em ambiente local controlado, com um conjunto específico de ferramentas e configurações
- Cenário hospitalar simulado de forma simplificada, sem emular concorrência real entre múltiplos clientes simultâneos
- Ausência de tráfego de arquivos DICOM de grande porte ou variações de topologia de rede

### Trabalhos futuros

- Ampliar a análise para ambientes distribuídos com **Mininet**
- Testar diferentes implementações de servidores
- Simular cargas de trabalho mais próximas da realidade hospitalar, incluindo transmissão paralela de exames de imagem por dezenas de usuários

### Conclusão geral

O HTTP/3 representa uma evolução importante em relação ao HTTP/1.1, oferecendo melhor desempenho e maior robustez em condições adversas de rede, principalmente devido às características do protocolo QUIC. No contexto hospitalar estudado, sua adoção mostra-se especialmente promissora para garantir a disponibilidade e a velocidade na transmissão de imagens médicas em situações de rede degradada, contribuindo para a continuidade e a qualidade do atendimento clínico.
