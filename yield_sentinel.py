import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def get_market_data():
    print("A aceder aos mercados financeiros...")
    # ^IRX = 13 Week Treasury Bill (Proxy para curto prazo/2Y)
    # ^TNX = 10 Year Treasury Note
    tickers = {"2Y": "^IRX", "10Y": "^TNX"}
    
    # Vamos buscar os dados do último ano
    data = yf.download(list(tickers.values()), period="1y")['Close']
    
    # Renomear as colunas para ser mais fácil de ler
    data.columns = ['10Y_Rate', '2Y_Rate']
    return data

def calculate_metrics(df):
    # O "Spread" é a diferença que o Gary Stevenson vigiava
    df['Spread'] = df['10Y_Rate'] - df['2Y_Rate']
    return df

def plot_sentinel(df):
    plt.figure(figsize=(12, 6))
    
    # Plot do Spread
    plt.plot(df.index, df['Spread'], label='Yield Spread (10Y - 2Y)', color='blue', lw=2)
    
    # Linha do Zero (Onde a curva inverte)
    plt.axhline(0, color='red', linestyle='--', label='Inversão da Curva (Recessão)')
    
    # Estética
    plt.title('The Yield Sentinel - Monitor de Recessão 2026', fontsize=15)
    plt.ylabel('Diferença em Pontos Percentuais')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print("A gerar gráfico...")
    plt.show()

if __name__ == "__main__":
    df_rates = get_market_data()
    df_metrics = calculate_metrics(df_rates)
    
    # Mostrar as últimas 5 linhas no terminal
    print("\nDados Recentes:")
    print(df_metrics.tail())
    
    plot_sentinel(df_metrics)