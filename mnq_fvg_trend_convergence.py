import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

## --- SETTINGS ---
SYMBOL = "MNQ=F"
INITIAL_CAPITAL = 50000
RISK_PER_TRADE = 600  
POINT_VALUE = 2.0
COMMISSION = 2.5
VAULT_FILE = "ema50_sma15_stats.csv"

def run_optimized_backtest():
    print(f"Fetching data for {SYMBOL}...")
    # Fetching 60 days of 5m data
    df = yf.download(SYMBOL, period="60d", interval="5m", progress=False)
    if df.empty: return
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    df.index = df.index.tz_convert('America/New_York')

    # 1. INDICATORS
    df['SMA15'] = df['Close'].rolling(window=15).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['Candle_Size'] = abs(df['High'] - df['Low'])
    df['Avg_Size'] = df['Candle_Size'].rolling(20).mean()

    # ICT FVG
    df['Bull_FVG'] = np.where(df['Low'] > df['High'].shift(2), df['High'].shift(2), np.nan)
    df['Bear_FVG'] = np.where(df['High'] < df['Low'].shift(2), df['Low'].shift(2), np.nan)

    ny_data = df.between_time("09:30", "15:55").copy()
    
    capital = INITIAL_CAPITAL
    equity_curve = [INITIAL_CAPITAL]
    time_series = [ny_data.index[0]] # For the graph x-axis
    trade_list = [] 
    
    active_bias = None
    entry_zone = None

    for i in range(20, len(ny_data)):
        row = ny_data.iloc[i]
        prev = ny_data.iloc[i-1]
        
        # LUNCH FILTER
        current_time = row.name.time()
        if datetime.strptime("12:00", "%H:%M").time() <= current_time <= datetime.strptime("13:30", "%H:%M").time():
            active_bias = None
            continue

        # BIAS DETECTION
        if prev['SMA15'] <= prev['EMA50'] and row['SMA15'] > row['EMA50'] and row['Close'] > row['EMA50']:
            fvg_lookback = ny_data['Bull_FVG'].iloc[i-3:i].dropna()
            if not fvg_lookback.empty: active_bias, entry_zone = 'Long', fvg_lookback.iloc[-1]
        elif prev['SMA15'] >= prev['EMA50'] and row['SMA15'] < row['EMA50'] and row['Close'] < row['EMA50']:
            fvg_lookback = ny_data['Bear_FVG'].iloc[i-3:i].dropna()
            if not fvg_lookback.empty: active_bias, entry_zone = 'Short', fvg_lookback.iloc[-1]

        # ENTRY EXECUTION
        if active_bias and entry_zone:
            if row['Candle_Size'] < (row['Avg_Size'] * 0.8): continue

            if (active_bias == 'Long' and row['Low'] <= entry_zone) or \
               (active_bias == 'Short' and row['High'] >= entry_zone):
                
                entry_p = entry_zone
                stop_dist = 25 
                t1_dist, t2_dist = stop_dist * 1.0, stop_dist * 5.0 
                
                current_stop = entry_p - stop_dist if active_bias == 'Long' else entry_p + stop_dist
                target1 = entry_p + t1_dist if active_bias == 'Long' else entry_p - t1_dist
                target2 = entry_p + t2_dist if active_bias == 'Long' else entry_p - t2_dist
                
                qty = int(RISK_PER_TRADE / (stop_dist * POINT_VALUE))
                if qty < 2: qty = 2 
                
                t1_hit, pnl, outcome_desc = False, 0, "LOSS"
                
                for j in range(i + 1, len(ny_data)):
                    low, high = ny_data['Low'].iloc[j], ny_data['High'].iloc[j]
                    
                    if active_bias == 'Long':
                        if not t1_hit and high >= target1:
                            t1_hit, current_stop, outcome_desc = True, entry_p, "T1_HIT_BE"
                            pnl += (qty/2) * t1_dist * POINT_VALUE
                        
                        if low <= current_stop:
                            if not t1_hit: pnl -= (qty * stop_dist * POINT_VALUE)
                            break
                        if high >= target2:
                            pnl += (qty/2) * t2_dist * POINT_VALUE
                            outcome_desc = "FULL_WIN"; break
                    else:
                        if not t1_hit and low <= target1:
                            t1_hit, current_stop, outcome_desc = True, entry_p, "T1_HIT_BE"
                            pnl += (qty/2) * t1_dist * POINT_VALUE
                            
                        if high >= current_stop:
                            if not t1_hit: pnl -= (qty * stop_dist * POINT_VALUE)
                            break
                        if low <= target2:
                            pnl += (qty/2) * t2_dist * POINT_VALUE
                            outcome_desc = "FULL_WIN"; break
                
                net_pnl = pnl - (qty * COMMISSION * 2)
                capital += net_pnl
                equity_curve.append(capital)
                time_series.append(ny_data.index[j])
                
                trade_list.append({
                    "Date": ny_data.index[i].strftime('%Y-%m-%d %H:%M'),
                    "Outcome": outcome_desc,
                    "Net_PnL": round(net_pnl, 2),
                    "Balance": round(capital, 2)
                })
                active_bias, entry_zone, i = None, None, j

    # --- RESULTS & GRAPHING ---
    if trade_list:
        log_df = pd.DataFrame(trade_list)
        log_df.to_csv(VAULT_FILE, index=False)
        
        # Stats for Console
        equity_series = pd.Series(equity_curve)
        max_dd = (equity_series - equity_series.cummax()).min()
        win_rate = (len(log_df[log_df['Net_PnL'] > 0]) / len(log_df)) * 100

        print(f"\nREPORT: {SYMBOL}")
        print(f"Profit: ${capital - INITIAL_CAPITAL:.2f} | Max DD: ${abs(max_dd):.2f} | WR: {win_rate:.2f}%")

        # Create Graph
        plt.style.use('dark_background') # Professional Look
        plt.plot(time_series, equity_curve, color='#00ffcc', linewidth=2, label="Equity")
        plt.fill_between(time_series, equity_curve, INITIAL_CAPITAL, color='#00ffcc', alpha=0.1)
        plt.axhline(y=INITIAL_CAPITAL, color='white', linestyle='--', alpha=0.3)
        plt.title(f"Trading Strategy Results - {SYMBOL}", fontsize=14)
        plt.ylabel("Account Balance ($)")
        plt.grid(axis='y', alpha=0.2)
        plt.tight_layout()
        plt.savefig('equity_curve.png')
        print("Graph saved as 'equity_curve.png'")
    else:
        print("No trades executed.")

if __name__ == "__main__":
    run_optimized_backtest()