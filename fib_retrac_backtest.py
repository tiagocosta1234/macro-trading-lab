import yfinance as yf
import pandas as pd
import numpy as np

# --- CHART BACKEND ADJUSTMENT ---
import matplotlib
try:
    matplotlib.use('TkAgg')
except:
    pass
import matplotlib.pyplot as plt
from datetime import datetime

## --- BACKTEST CONFIGURATION ---
SYMBOL = "MNQ=F"
INITIAL_CAPITAL = 100000
CONTRACTS = 3            
POINT_VALUE = 2.0        
COMMISSION = 2.50        

def run_pure_backtest():
    print(f"INITIALIZING PURE QUANTITATIVE BACKTEST ENGINE - {SYMBOL}")
    print("═"*70)

    # 1. MULTI-TIMEFRAME DATA DOWNLOAD
    print("Loading...")
    df_15m = yf.download(SYMBOL, period="60d", interval="15m", group_by='column', progress=False)
    df_1h = yf.download(SYMBOL, period="60d", interval="1h", group_by='column', progress=False)
    
    if df_15m.empty or df_1h.empty:
        print("Data fetch failed from Yahoo Finance.")
        return

    # Column Standardization
    for df in [df_15m, df_1h]:
        if isinstance(df.columns, pd.MultiIndex):
            if 'High' in df.columns.get_level_values(0):
                df.columns = df.columns.get_level_values(0)
            else:
                df.columns = df.columns.get_level_values(1)
        df.columns = [str(col).strip().capitalize() for col in df.columns]
        df.index = df.index.tz_convert('America/New_York')

    # 2. CALCULATE 1H SWING HIGHS (Exit Targets)
    df_1h['Swing_High'] = np.where(
        (df_1h['High'] > df_1h['High'].shift(1)) & (df_1h['High'] > df_1h['High'].shift(2)) &
        (df_1h['High'] > df_1h['High'].shift(-1)) & (df_1h['High'] > df_1h['High'].shift(-2)),
        df_1h['High'], np.nan
    )
    df_1h['Swing_High'] = df_1h['Swing_High'].ffill()

    # 3. IDENTIFY 15M ORDER BLOCKS
    df_15m['Is_Down_Candle'] = df_15m['Close'] < df_15m['Open']
    df_15m['OB_Top'] = np.where(df_15m['Is_Down_Candle'] & (df_15m['Close'].shift(-1) > df_15m['Open']), df_15m['High'], np.nan)
    df_15m['OB_Bottom'] = np.where(df_15m['Is_Down_Candle'] & (df_15m['Close'].shift(-1) > df_15m['Open']), df_15m['Low'], np.nan)
    df_15m['OB_Top'] = df_15m['OB_Top'].ffill()
    df_15m['OB_Bottom'] = df_15m['OB_Bottom'].ffill()

    # 4. RETRACEMENT LEGS & 79% OTE FIB LEVEL
    df_15m['Range_High'] = df_15m['High'].rolling(window=20).max()
    df_15m['Range_Low'] = df_15m['Low'].rolling(window=20).min()
    df_15m['Fib_79'] = df_15m['Range_High'] - (df_15m['Range_High'] - df_15m['Range_Low']) * 0.79

    # Portfolio Tracking Variables
    capital = INITIAL_CAPITAL
    equity_curve = [INITIAL_CAPITAL]
    trade_pnl_list = []
    risk_taken_list = []
    rr_ratios_list = [] 
    
    in_position = False
    entry_p = 0
    stop_p = 0
    target_p = 0

    # Static High-Impact News Embargo (10:00 AM & 2:00 PM EST)
    FORBIDDEN_TIMES = [
        datetime.strptime("09:45", "%H:%M").time(),
        datetime.strptime("10:00", "%H:%M").time(),
        datetime.strptime("13:45", "%H:%M").time(),
        datetime.strptime("14:00", "%H:%M").time()
    ]

    # 5. BACKTEST ENGINE LOOP
    for i in range(20, len(df_15m)):
        row_15m = df_15m.iloc[i]
        t_stamp = df_15m.index[i]
        current_time = t_stamp.time()
        
        # 1H Macro Context Filter
        h1_matches = df_1h.loc[df_1h.index <= t_stamp]
        if h1_matches.empty: continue
        current_1h_swing = h1_matches['Swing_High'].iloc[-1]
        if pd.isna(current_1h_swing): continue

        is_ny = (datetime.strptime("09:30", "%H:%M").time() <= current_time <= datetime.strptime("16:00", "%H:%M").time())
        is_tokyo = (datetime.strptime("19:00", "%H:%M").time() <= current_time) or (current_time <= datetime.strptime("02:00", "%H:%M").time())
        is_news_embargo = current_time in FORBIDDEN_TIMES
        
        if not in_position:
            # Entry Trigger
            if (is_ny or is_tokyo) and not is_news_embargo and (row_15m['Low'] <= row_15m['Fib_79'] < row_15m['Close']):
                
                # Institutional Verification (79% inside the 15m Order Block)
                is_inside_ob = (row_15m['OB_Bottom'] <= row_15m['Fib_79'] <= row_15m['OB_Top'])
                
                if is_inside_ob:
                    in_position = True
                    entry_p = row_15m['Fib_79']
                    stop_p = row_15m['Range_Low']
                    target_p = current_1h_swing
                    
                    if entry_p <= stop_p or target_p <= entry_p:
                        in_position = False
                        continue
                    
                    # Record Setup Metrics
                    risk_points = entry_p - stop_p
                    reward_points = target_p - entry_p
                    
                    rr_ratios_list.append(reward_points / risk_points)
                    risk_taken_list.append(risk_points * POINT_VALUE * CONTRACTS)
        
        else:
            # Exit Logic and Risk Management
            is_eod = current_time in [datetime.strptime("15:45", "%H:%M").time(), datetime.strptime("01:45", "%H:%M").time()]
            
            if is_eod:  # End of Day Forced Close
                net_pnl = ((row_15m['Close'] - entry_p) * POINT_VALUE * CONTRACTS) - (CONTRACTS * COMMISSION)
                capital += net_pnl
                equity_curve.append(capital)
                trade_pnl_list.append(net_pnl)
                in_position = False
                
            elif row_15m['Low'] <= stop_p:  # Stop Loss Hit
                net_pnl = -((entry_p - stop_p) * POINT_VALUE * CONTRACTS) - (CONTRACTS * COMMISSION)
                capital += net_pnl
                equity_curve.append(capital)
                trade_pnl_list.append(net_pnl)
                in_position = False
                
            elif row_15m['High'] >= target_p:  # Take Profit Hit (1H Swing High)
                net_pnl = ((target_p - entry_p) * POINT_VALUE * CONTRACTS) - (CONTRACTS * COMMISSION)
                capital += net_pnl
                equity_curve.append(capital)
                trade_pnl_list.append(net_pnl)
                in_position = False

    # --- PURE PERFORMANCE METRICS ---
    if trade_pnl_list:
        pnl_series = pd.Series(trade_pnl_list)
        equity_series = pd.Series(equity_curve)
        
        total_profit = capital - INITIAL_CAPITAL
        win_rate = (len(pnl_series[pnl_series > 0]) / len(pnl_series)) * 100
        max_dd = abs((equity_series - equity_series.cummax()).min())
        avg_rr = np.mean(rr_ratios_list) if rr_ratios_list else 0
        profit_factor = abs(pnl_series[pnl_series > 0].sum() / pnl_series[pnl_series < 0].sum()) if len(pnl_series[pnl_series < 0]) > 0 else np.inf

        print(f"Backtest Window:      {df_15m.index.min().strftime('%Y-%m-%d')} to {df_15m.index.max().strftime('%Y-%m-%d')}")
        print("═"*70)
        print(f"Total Net Profit:     ${total_profit:.2f}")
        print(f"Max Historical DD:    ${max_dd:.2f}")
        print(f"Profit Factor:        {profit_factor:.2f}")
        print(f"Avg Risk:Reward Ratio: 1:{avg_rr:.2f}")
        print(f"Win Rate:             {win_rate:.2f}%")
        print(f"Total Trades:         {len(pnl_series)}")
        print(f"Final Balance:         ${capital:.2f}")
        print("═"*70)

        # Standard Performance Curve Graph
        plt.style.use('dark_background')
        fig, ax = plt.subplots(num="Pure Quantitative Backtest Engine", figsize=(10, 5))
        ax.plot(equity_curve, color='#00ffcc', linewidth=2, label='Net Equity Curve')
        ax.axhline(y=INITIAL_CAPITAL, color='white', linestyle='--', alpha=0.3)
        ax.set_title(f"Historical Quantitative Performance - {SYMBOL}")
        ax.set_xlabel("Executed Trades")
        ax.set_ylabel("Capital ($)")
        ax.legend(loc="upper left")
        ax.grid(True, linestyle=':', alpha=0.2)
        
        plt.draw()
        plt.pause(0.001)
        plt.show(block=True)
    else:
        print("Scanned historical data but 0 entries met all institutional parameters.")

if __name__ == "__main__":
    run_pure_backtest()