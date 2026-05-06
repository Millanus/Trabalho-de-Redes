# Trabalho de Redes de Computadores
### Integrantes:
Guilherme Dornelles Guarienti Millani (2510200473) – Líder

Iago Leão Silveira de Souza (2010200689)
### 1. Introdução
O protocolo HTTP (Hypertext Transfer Protocol) é a base da World Wide Web, permitindo a comunicação entre clientes e servidores. Com o crescimento das aplicações web, que passaram a exigir maior velocidade e segurança, tornou-se necessário evoluir os protocolos de comunicação para suportar conexões mais eficientes e criptografadas.

Com isso, o HTTP/1.1 apresenta limitações de desempenho, como o problema de bloqueio de início de linha (Head-of-Line Blocking) e overhead de conexão. Além disso, embora o HTTP/3 traga melhorias de desempenho em cenários com perda de pacotes por meio do uso do protocolo QUIC, ainda há relativamente poucos estudos comparativos diretos entre HTTP/3 e HTTP/1.1 em cenários variados de rede, o que dificulta uma análise mais clara sobre quando sua adoção é mais vantajosa.
### 2. Proposta
Este trabalho propõe uma análise comparativa entre os protocolos HTTP/1.1 e HTTP/3. A proposta é medir métricas como latência (RTT) e tempo de carregamento de páginas (Page Load Time) em um ambiente controlado, simulando diferentes condições de rede, como atraso e perda de pacotes, para avaliar os ganhos de desempenho do HTTP/3.

Para isso, serão utilizadas tecnologias como Docker, para a criação de ambientes isolados e reprodutíveis, e ferramentas de controle de rede como o tc (Traffic Control), permitindo a simulação de diferentes condições de rede. A coleta de dados será realizada por meio de scripts em Python, utilizando bibliotecas compatíveis com QUIC e a biblioteca padrão socket para conexões HTTP/1.1, garantindo a repetibilidade dos experimentos. Além disso, serão empregados o Wireshark para análise detalhada do tráfego de rede e o Mininet para a emulação de topologias de rede controladas, possibilitando a observação do comportamento dos protocolos em diferentes cenários.
