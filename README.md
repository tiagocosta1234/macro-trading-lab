# Macro Trading Lab

Este repositório é um laboratório pessoal dedicado à exploração de modelos macroeconómicos, análise quantitativa e desenvolvimento de algoritmos de trading utilizando Python. O foco principal é a conversão de teorias financeiras em sistemas de backtesting robustos e ferramentas de monitorização em tempo real.

O projeto integra princípios de engenharia de software com análise de séries temporais, permitindo uma visão técnica sobre ativos de renda fixa e moedas.

## Estrutura do Repositório

O laboratório está organizado nos seguintes módulos principais:

### 1. Yield Sentinel & SMA Backtest
Estudo focado no momentum das taxas de juro de longo prazo dos EUA.
*   **Ficheiros**: `yield_sentinel.py`, `sma_backtest.py`
*   **Estratégia**: Análise de tendência baseada no cruzamento de Médias Móveis Simples (SMA) sobre a Yield de 10 anos (^TNX).
*   **Objetivo**: Identificar mudanças de ciclo nas taxas de juro e avaliar a eficácia de estratégias de seguimento de tendência.

### 2. Euro Sentinel
Módulo dedicado à análise do par de moedas EUR/USD e indicadores da Zona Euro.
*   **Ficheiro**: `euro_sentinel.py`
*   **Objetivo**: Monitorizar a força relativa do Euro e analisar o impacto de diferenciais de taxas de juro e dados macroeconómicos europeus na taxa de câmbio.

### 3. Main Dashboard
A interface central de visualização do laboratório.
*   **Ficheiro**: `main_dashboard.py`
*   **Funcionalidade**: Consolida as métricas dos vários sentinelas numa única visualização gráfica, permitindo uma análise comparativa rápida entre Yields, Moedas e a performance das estratégias.

## Tecnologias Utilizadas

*   **Python 3.x**: Linguagem principal.
*   **Pandas**: Processamento de dados e cálculo de indicadores estatísticos.
*   **YFinance**: Extração de dados históricos e em tempo real do Yahoo Finance.
*   **Matplotlib / Plotly**: Motores gráficos para visualização de performance e dashboards.

## Como Executar

1. Clonar o repositório:
   ```bash
   git clone [https://github.com/TEU-UTILIZADOR/macro-trading-lab.git](https://github.com/TEU-UTILIZADOR/macro-trading-lab.git)
