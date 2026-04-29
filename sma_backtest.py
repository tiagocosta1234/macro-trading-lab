import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def run_sma_backtest():
    # 1. Initial Configurations
    ticker = "MNQ=F"  # E-micro Nasdaq 100 Futures
    start_date = "2020-01-01"
    end_date = "2026-04-25"
    initial_capital = 100000
    
    # Micro Contract Parameters (MNQ)
    n_contracts = 5  # Number of micro contracts to trade
    point_value = 2  # 1 point in MNQ = $2
    dollar_per_point = n_contracts * point_value
    daily_loss_limit = -0.04 # 4% Daily Loss Limit

    print(f"--- Quantitative Backtest: {ticker} (5 Micros) ---")

    # 2. Data Download
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty: 
        print("Error: No data found.")
        return None

    # Clean columns in case of MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 3. SMA Strategy: SMA(10) vs SMA(30)
    data['SMA_Fast'] = data['Close'].rolling(window=10).mean()
    data['SMA_Slow'] = data['Close'].rolling(window=30).mean()
    data['Signal'] = (data['SMA_Fast'] > data['SMA_Slow']).astype(int)

    # 4. PnL Calculation (Point-based)
    data['Point_Change'] = data['Close'].diff()
    data['Daily_PnL'] = data['Signal'].shift(1) * data['Point_Change'] * dollar_per_point

    # 5. Risk Management: Daily Loss Limit (4%)
    capital_prev = initial_capital
    pnl_protected = []
    
    for i in range(len(data)):
        # Calculate daily return relative to accumulated capital
        daily_return_pct = data['Daily_PnL'].iloc[i] / capital_prev if capital_prev > 0 else 0
        
        if daily_return_pct <= daily_loss_limit:
            # Trigger daily stop at exactly 4% of previous day's capital
            actual_pnl = capital_prev * daily_loss_limit
        else:
            actual_pnl = data['Daily_PnL'].iloc[i]
            
        pnl_protected.append(actual_pnl)
        capital_prev += actual_pnl

    data['Daily_PnL_Final'] = pnl_protected

    # 6. Equity Curve Evolution
    data['Strategy_Equity'] = data['Daily_PnL_Final'].cumsum() + initial_capital
    data['Buy_Hold_Equity'] = (data['Close'] / data['Close'].iloc[0]) * initial_capital

    # 7. Signal Markers for Plotting
    data['Buy_Marker'] = np.where((data['Signal'] == 1) & (data['Signal'].shift(1) == 0), data['Strategy_Equity'], np.nan)
    data['Sell_Marker'] = np.where((data['Signal'] == 0) & (data['Signal'].shift(1) == 1), data['Strategy_Equity'], np.nan)

    # 8. Performance Metrics
    final_strategy = data['Strategy_Equity'].iloc[-1]
    final_buy_hold = data['Buy_Hold_Equity'].iloc[-1]
    max_dd = ((data['Strategy_Equity'] - data['Strategy_Equity'].cummax()) / data['Strategy_Equity'].cummax()).min() * 100
    
    # New: Leverage Metrics
    current_price = data['Close'].iloc[-1]
    notional_exposure = current_price * point_value * n_contracts
    leverage = notional_exposure / final_strategy

    print("-" * 40)
    print(f"FINAL RESULTS ({start_date} to {end_date})")
    print(f"Final Strategy Equity:  ${final_strategy:,.2f}")
    print(f"Final Buy & Hold Equity: ${final_buy_hold:,.2f}")
    print(f"Absolute Difference:     ${(final_strategy - final_buy_hold):,.2f}")
    print(f"Max Strategy Drawdown:   {max_dd:.2f}%")
    print("-" * 40)
    print(f"Current Market Value Controlled: ${notional_exposure:,.2f}")
    print(f"Current Account Leverage:        {leverage:.2f}x")
    print("-" * 40)
    
    # 9. Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(data['Strategy_Equity'], label='Strategy (5 Micros MNQ)', color='green', lw=2)
    plt.plot(data['Buy_Hold_Equity'], label='Buy & Hold Baseline', color='gray', linestyle='--', alpha=0.7)
    
    # Plot Entry/Exit Markers
    plt.scatter(data.index, data['Buy_Marker'], marker='^', color='lime', s=100, label='Long Entry', zorder=5)
    plt.scatter(data.index, data['Sell_Marker'], marker='v', color='red', s=100, label='Exit (Flat)', zorder=5)
    
    plt.title(f'MNQ=F: SMA Strategy vs Buy & Hold (Leveraged Approach)')
    plt.ylabel('Account Value ($)')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return data

if __name__ == "__main__":
    run_sma_backtest()