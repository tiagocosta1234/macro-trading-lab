from yield_sentinel import get_market_data as get_yield_data
from euro_sentinel import get_euro_spread

def get_data():
    print("A recolher indicadores... (Sincronizando com original)")
    # Usando T-Bill 13 semanas (^IRX) e 10Y (^TNX)
    # Nota: Se falhar, o script avisa
    tickers = ["^TNX", "^IRX", "LQD", "TLT"]
    try:
        data = yf.download(tickers, period="1y")['Close']
        return data
    except Exception as e:
        print(f"Erro no download: {e}")
        return None

def show_dashboard(df):
    if df is None or df.empty:
        print("Sem dados para exibir.")
        return

    print("Colunas recebidas:", df.columns.tolist())

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- GRÁFICO 1: YIELD CURVE ---
    if '^TNX' in df.columns and '^IRX' in df.columns:
        spread = df['^TNX'] - df['^IRX']

        ax1.plot(df.index, spread, color='blue', label='Spread (10Y-3M)')
        ax1.axhline(spread.mean(), color='grey', linestyle='--', label='Média')
    else:
        ax1.text(0.5, 0.5, 'Erro: Tickers ^TNX ou ^IRX não encontrados', ha='center')

    ax1.axhline(0, color='red', linestyle='-')
    ax1.set_title('EUA: Monitor de Yield')
    ax1.grid(True, alpha=0.2)
    ax1.legend()

    # --- GRÁFICO 2: STRESS DE CRÉDITO ---
    if 'LQD' in df.columns and 'TLT' in df.columns:
        ratio = df['LQD'] / df['TLT']
        ax2.plot(df.index, ratio, color='salmon', alpha=0.4)
        ax2.plot(df.index, ratio.rolling(20).mean(), color='red', lw=2, label='Tendência')
        ax2.set_title('Global: Stress de Crédito (LQD/TLT)')
        ax2.grid(True, alpha=0.2)
        ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = get_data()
    show_dashboard(data)
