import yfinance as yf
import matplotlib.pyplot as plt

def get_euro_spread():
    print("A usar Tickers de Alta Disponibilidade (ETFs de Rendimento)...")
    
    # TLT = Obrigações do Tesouro (Segurança)
    # LQD = Obrigações de Empresas (Risco de Crédito)
    # Quando o LQD cai face ao TLT, o stress financeiro está a subir.
    tickers = {
        "Seguranca": "TLT", 
        "Risco": "LQD"
    }
    
    data = yf.download(list(tickers.values()), period="1y")['Close']
    return data

def plot_euro_risk(df):
    # Garante que existem dados antes de tentar desenhar
    if df.empty:
        print("Erro: O DataFrame está vazio. Verifica a ligação à internet.")
        return

    plt.figure(figsize=(12, 6))
    
    # Criar o rácio
    stress_ratio = df['LQD'] / df['TLT']
    
    plt.plot(df.index, stress_ratio, color='red', lw=2, label='Rácio de Risco (LQD/TLT)')
    plt.title('Global Financial Stress Monitor', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    print("A abrir a janela do gráfico...")
    plt.show(block=True) 

if __name__ == "__main__":
    df_euro = get_euro_spread()
    
    # Verifica se o download funcionou antes de tentar desenhar
    if not df_euro.empty:
        print("Dados obtidos com sucesso. A abrir gráfico...")
        plot_euro_risk(df_euro)
    else:
        print("Erro: O Yahoo não devolveu dados.")
