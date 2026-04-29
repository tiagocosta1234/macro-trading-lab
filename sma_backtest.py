import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def run_sma_backtest():
    # 1. Configurações Iniciais
    ticker = "^TNX"  # Yields do Tesouro EUA a 10 anos
    start_date = "2020-01-01"
    end_date = "2026-04-20"
    initial_capital = 100000  # Capital inicial de 1 milhão de euros

    print(f"--- Backtest para {ticker} ---")

    # 2. Download de Dados
    # O yfinance devolve um DataFrame com os preços históricos
    data = yf.download(ticker, start=start_date, end=end_date)
    
    if data.empty:
        print("Erro: Não foi possível obter dados. Verifica a tua ligação à internet.")
        return

    # 3. Definição da Estratégia (Lógica do Sentinel)
    # Dduas médias móveis para identificar a tendência
    window_fast = 10
    window_slow = 30
    
    data['SMA_Fast'] = data['Close'].rolling(window=window_fast).mean()
    data['SMA_Slow'] = data['Close'].rolling(window=window_slow).mean()

    # Gerar Sinais: 
    # 1 (Compra/Long) quando a média curta está acima da longa
    # 0 (Fora do Mercado) quando está abaixo
    data['Signal'] = (data['SMA_Fast'] > data['SMA_Slow']).astype(int)

    # 4. Cálculo de Retornos
    # Retorno diário do ativo (percentagem de variação)
    data['Asset_Returns'] = data['Close'].pct_change()

    # Retorno da Estratégia:
    data['Strategy_Returns'] = data['Signal'].shift(1) * data['Asset_Returns']

    # 5. Cálculo da Equity Curve (Evolução do Capital)
    # O capital cresce de forma composta: (1 + r1) * (1 + r2) ...
    data['Strategy_Equity'] = (1 + data['Strategy_Returns'].fillna(0)).cumprod() * initial_capital
    data['Buy_Hold_Equity'] = (1 + data['Asset_Returns'].fillna(0)).cumprod() * initial_capital

    # 6. Métricas de Performance
    final_value = data['Strategy_Equity'].iloc[-1]
    total_return = (final_value / initial_capital - 1) * 100
    data['Peak'] = data['Strategy_Equity'].cummax()
    data['Drawdown'] = (data['Strategy_Equity'] - data['Peak']) / data['Peak']
    max_dd = data['Drawdown'].min() * 100
    
    print(f"Capital Inicial: {initial_capital:.2f}€")
    print(f"Capital Final: {final_value:.2f}€")
    print(f"Retorno Total: {total_return:.2f}%")
    print(f"Max Drawdown: {max_dd:.2f}%")

    # 7. Visualização Gráfica
    plt.figure(figsize=(12, 6))
    plt.plot(data['Strategy_Equity'], label='Estratégia Yield Sentinel', color='blue', linewidth=2)
    plt.plot(data['Buy_Hold_Equity'], label='Buy & Hold (Referência)', color='gray', linestyle='--')
    
    plt.title(f'Backtesting: SMA approach vs Buy & Hold ({ticker})')
    plt.xlabel('Data')
    plt.ylabel('Valor da Carteira (€)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Executar o backtesting   
if __name__ == "__main__":
    run_sma_backtest()
