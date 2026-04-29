# Macro Trading Lab

Este repositório é um laboratório pessoal dedicado à exploração de modelos macroeconómicos, análise quantitativa e desenvolvimento de algoritmos de trading utilizando Python. O foco principal é a conversão de teorias financeiras em sistemas de backtesting robustos e mensuráveis.

O projeto foi desenvolvido no contexto de aprendizagem académica e técnica (FCUL), integrando princípios de engenharia de software com análise de séries temporais financeiras.

## Visão Geral

O Macro Trading Lab serve como uma plataforma para testar hipóteses sobre o comportamento dos mercados, com especial atenção ao mercado de dívida soberana (Yields) e à sua influência nos ativos de risco.

## Estrutura do Repositório

O repositório está organizado por módulos de estratégia, permitindo a comparação entre diferentes abordagens algorítmicas:

### 1. Yield Sentinel (SMA Edition)
O primeiro módulo do laboratório foca-se no "momentum" das taxas de juro de longo prazo.
*   **Ficheiro**: `sma_backtest.py`
*   **Ativo Base**: US 10-Year Treasury Yield (^TNX).
*   **Estratégia**: Cruzamento de Médias Móveis Simples (SMA). Utiliza uma janela curta de 10 dias e uma janela longa de 30 dias para gerar sinais de entrada e saída.
*   **Objetivo**: Validar se uma estratégia simples de seguimento de tendência consegue proteger capital durante períodos de volatilidade nas taxas de juro.

## Tecnologias e Dependências

O projeto utiliza a stack padrão de Data Science em Python:

*   **Python 3.x**: Linguagem base.
*   **Pandas**: Processamento de dados e cálculo de indicadores estatísticos.
*   **YFinance**: Interface para extração de dados históricos do Yahoo Finance.
*   **Matplotlib**: Motor gráfico para visualização de performance e curvas de capital (Equity Curves).

## Instalação e Utilização

1. Clonar o repositório:
   ```bash
   git clone [https://github.com/tiagocosta1234/macro-trading-lab.git](https://github.com/tiagocosta1234/macro-trading-lab.git)
