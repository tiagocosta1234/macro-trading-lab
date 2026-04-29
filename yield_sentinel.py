# Este projeto monitoriza o diferencial entre as taxas de juro de 2 e 10 anos.
# Quando o spread inverte, historicamente, uma recessão ocorre nos 12-18 meses seguintes.

import yfinance as yf
import matplotlib.pyplot as plt

def get_market_data():
    print("A aceder aos mercados financeiros...")
    
    # ^TNX = 10 Anos
    # ^IRX = 3 Meses (O Yahoo entrega este sempre)

    tickers = {"5Y": "^FVX", "10Y": "^TNX"}
    
    data = yf.download(list(tickers.values()), period="1y")['Close']
    
    # Garantir a ordem das colunas
    data = data.rename(columns={"^FVX": "Short_Rate", "^TNX": "10Y_Rate"})
    return data

def calculate_metrics(df):
    # Se a Short_Rate (5Y) for maior que a 10Y, o gráfico desce para o negativo
    df['Spread'] = df['10Y_Rate'] - df['Short_Rate']
    return df

def plot_sentinel(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Spread'], label='Yield Spread (10Y - 5Y)', color='blue', lw=2)
    plt.axhline(0, color='red', linestyle='--', label='Inversão (Recessão)')
    
    plt.title('The Yield Sentinel - Spread 10Y-5Y', fontsize=15)
    plt.ylabel('Diferença (Points)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    df = get_market_data()
    if not df.empty:
        df = calculate_metrics(df)
        print(df.tail())
        plot_sentinel(df)
