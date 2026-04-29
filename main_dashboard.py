import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def get_data():
    tickers = ["^TNX", "^IRX", "LQD", "TLT"]
    try:
        df = yf.download(tickers, period="1y")['Close']
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception as e:
        print(f"Erro no download: {e}")
        return None

def show_dashboard(df):
    if df is None or df.empty:
        print("Erro: DataFrame vazio.")
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- GRÁFICO 1: YIELD CURVE ---
    if '^TNX' in df.columns and '^IRX' in df.columns:
        yield_spread = df['^TNX'] - df['^IRX']
        ax1.plot(df.index, yield_spread, color='blue', label='Spread (10Y-3M)')
        ax1.axhline(yield_spread.mean(), color='grey', linestyle='--', label='Média')
        ax1.axhline(0, color='red', linestyle='-')
        ax1.set_title('EUA: Monitor de Yield')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
    
    # --- GRÁFICO 2: STRESS DE CRÉDITO ---
    if 'LQD' in df.columns and 'TLT' in df.columns:
        credit_ratio = df['LQD'] / df['TLT']
        ax2.plot(df.index, credit_ratio, color='salmon', alpha=0.4)
        ax2.plot(df.index, credit_ratio.rolling(20).mean(), color='red', lw=2, label='Tendência')
        ax2.set_title('Global: Stress de Crédito (LQD/TLT)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("A carregar Dashboard Macro...")
    data_macro = get_data()
    show_dashboard(data_macro)