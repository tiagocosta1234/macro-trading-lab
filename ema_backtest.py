import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def run_ema_backtest():
    # 1. Initial Configurations
    ticker = "MNQ=F"
    start_date = "2020-01-01"
    end_date = "2026-04-29"
    initial_capital = 100000
    
    # Micro Contract Parameters (MNQ)
    n_contracts = 5
    point_value = 2  
    dollar_per_point = n_contracts * point_value 
    daily_loss_limit = -0.04 

    print(f"--- Quantitative EMA Backtest: {ticker} (5 Micros) ---")

    # 2. Data Download
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty: return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 3. EMA Strategy: Faster reaction to price action
    # .ewm(span=X) for Exponential Moving Average
    data['EMA_Fast'] = data['Close'].ewm(span=10, adjust=False).mean()
    data['EMA_Slow'] = data['Close'].ewm(span=30, adjust=False).mean()
    data['Signal'] = (data['EMA_Fast'] > data['EMA_Slow']).astype(int)

    # 4. PnL Calculation
    data['Point_Change'] = data['Close'].diff()
    data['Daily_PnL'] = data['Signal'].shift(1) * data['Point_Change'] * dollar_per_point

    # 5. Risk Management (Daily Stop Loss)
    capital_prev = initial_capital
    pnl_protected = []
    
    for i in range(len(data)):
        daily_return_pct = data['Daily_PnL'].iloc[i] / capital_prev if capital_prev > 0 else 0
        if daily_return_pct <= daily_loss_limit:
            actual_pnl = capital_prev * daily_loss_limit
        else:
            actual_pnl = data['Daily_PnL'].iloc[i]
        pnl_protected.append(actual_pnl)
        capital_prev += actual_pnl

    data['Daily_PnL_Final'] = pnl_protected

    # 6. Equity Curve Evolution
    data['Strategy_Equity'] = data['Daily_PnL_Final'].cumsum() + initial_capital
    data['Buy_Hold_Equity'] = (data['Close'] / data['Close'].iloc[0]) * initial_capital

    # 7. Signal Markers
    data['Buy_Marker'] = np.where((data['Signal'] == 1) & (data['Signal'].shift(1) == 0), data['Strategy_Equity'], np.nan)
    data['Sell_Marker'] = np.where((data['Signal'] == 0) & (data['Signal'].shift(1) == 1), data['Strategy_Equity'], np.nan)

    # 8. Final Metrics
    final_strategy = data['Strategy_Equity'].iloc[-1]
    final_buy_hold = data['Buy_Hold_Equity'].iloc[-1]
    max_dd = ((data['Strategy_Equity'] - data['Strategy_Equity'].cummax()) / data['Strategy_Equity'].cummax()).min() * 100
    
    current_price = data['Close'].iloc[-1]
    notional_exposure = current_price * point_value * n_contracts
    leverage = notional_exposure / final_strategy

    print("-" * 40)
    print(f"FINAL RESULTS (EMA Approach)")
    print(f"Final Strategy Equity:  ${final_strategy:,.2f}")
    print(f"Final Buy & Hold Equity: ${final_buy_hold:,.2f}")
    print(f"Max Strategy Drawdown:   {max_dd:.2f}%")
    print("-" * 40)
    print(f"Notional Exposure:       ${notional_exposure:,.2f}")
    print(f"Account Leverage:        {leverage:.2f}x")
    print("-" * 40)
    
    # 9. Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(data['Strategy_Equity'], label='EMA Strategy (5 MNQ)', color='royalblue', lw=2)
    plt.plot(data['Buy_Hold_Equity'], label='Buy & Hold Baseline', color='gray', linestyle='--', alpha=0.6)
    
    plt.scatter(data.index, data['Buy_Marker'], marker='^', color='lime', s=100, label='EMA Cross Up', zorder=5)
    plt.scatter(data.index, data['Sell_Marker'], marker='v', color='red', s=100, label='EMA Cross Down', zorder=5)
    
    plt.title(f'MNQ=F: Exponential Moving Average (10/30) Strategy')
    plt.ylabel('Account Value ($)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return data

if __name__ == "__main__":
    run_ema_backtest()