# Macro Trading Lab

This repository is a personal laboratory dedicated to the exploration of macroeconomic models, quantitative analysis, and the development of algorithmic trading systems using Python.

## Repository Structure

The laboratory is organized into the following primary modules:

## 1. Futures Backtesting Engines (Nasdaq / MNQ)
Quantitative simulators focused on Nasdaq-100 Micro Futures contracts (**MNQ=F**).

* **SMA Strategy (`sma_backtest.py`)**: A classic Simple Moving Average (10/30) crossover implementation. This serves as the foundational baseline and historical benchmark for the laboratory.
* **EMA Strategy (`ema_backtest.py`)**: A technical evolution utilizing Exponential Moving Averages (10/30). This version reacts significantly faster to price pivots, reducing the inherent lag of simple averages.
* **Volatility Adjusted Strategy (`volat_adjusted_backtest.py`)**: The most advanced moving-average model in the lab. It leverages a vectorized architecture to process high-density data (2020-2026) and implements **Volatility Equalization**. Position sizing is dynamically adjusted via the Average True Range (ATR), ensuring a constant dollar risk regardless of fluctuating market volatility.
* **MNQ FVG Trend Convergence (`mnq_fvg_trend_convergence.py`)**: 
    A high-precision hybrid strategy merging trend convergence with Institutional Price Action (ICT).
    * **Entry Logic:** Aligns macro trend via **SMA15/EMA50** while executing entries on **Fair Value Gaps (FVG)** during high-volatility windows (New York session).
    * **Dual-Target System:** Implements an asymmetrical trade management protocol. Half the position is closed at a 1:1 risk-to-reward ratio (securing rapid break-even), while a runner targets a **5:1 (Reward/Risk)** payout to capture prolonged trends.
    * **Forensics:** Automatically plots capital growth (`equity_curve.png`) and logs detailed trade data for post-mortem performance analysis.
* **Institutional OTE Engine (`fib_retrac_backtest.py`)**: A pure quantitative engine built entirely on *Smart Money Concepts* (ICT) and Multi-Timeframe Analysis. It maps 15-minute *Order Blocks* and executes entries at the 79% Optimal Trade Entry (OTE) Fibonacci retracement level, using 1-hour *Swing Highs* as liquidity targets. It includes detailed, automated tracking of the structural Risk:Reward ratio per operation.
* **Lucid Prop-Firm Simulator (`fib_retrac_lucid.py`)**: An advanced derivation of the OTE engine, heavily engineered to stress-test the strategy against strict Prop-Firm regulations (specifically the **Lucid 100k Flex Challenge**). It features professional guardrails including a strict $3,000 *Max Drawdown* limit, a $6,000 profit target, forced End-of-Day (EOD) position liquidation, and an algorithmic news embargo that blocks trading during high-impact macroeconomic data releases.

* **Risk Management Protocols**: 
    * In the initial strategies (**SMA/EMA**), risk management is static, operating with a fixed 5 Micro contracts and a 4% daily loss limit.
    * In the **Volatility Adjusted Strategy**, risk is dynamically sized based on nominal fiat risk: the system calculates contract lot sizes based on current volatility (ATR), risking a fixed dollar amount (e.g., $4,000) per unit of deviation. This optimizes the Sharpe ratio by surviving choppy markets and capitalizing on strong trends.
    * In the institutional algorithms (**OTE / Lucid**), risk is evaluated on a structural basis (measuring the precise point distance from the entry to the invalidation point at the bottom of the *Order Block*) and enforces strict compliance with execution time limits and geographic session filters.

### 2. Market Sentinels
Real-time monitoring tools for various asset classes and macroeconomic indicators.

* **Main Dashboard (`main_dashboard.py`)**: A comprehensive visualizer for leading macro indicators, prominently featuring the **Yield Curve Spread (10Y-3M)** and the corporate credit stress ratio (**LQD/TLT**).
* **Yield Sentinel (`yield_sentinel.py`)**: A specialized monitor dedicated to analyzing sovereign yield curves and their downstream impact on the cost of capital.
* **Euro Sentinel (`euro_sentinel.py`)**: Tracks the **EUR/USD** forex pair, analyzing the relative strength of the European currency against the Dollar.

---

## Core Quantitative & Theoretical Concepts

The algorithms in this laboratory are built upon several advanced trading methodologies, spanning from traditional quantitative math to modern institutional footprint reading:

### Algorithmic & Quantitative Models
* **Vectorization:** Instead of iterating through historical data row-by-row, operations are mathematically applied to entire datasets simultaneously using Pandas and NumPy. This drastically reduces computation time for multi-year backtests.
* **Volatility Equalization (ATR Sizing):** A risk-parity concept where position sizes are inversely scaled to current market volatility (measured by the Average True Range). In chaotic markets, contract sizes shrink; in quiet markets, they expand, keeping the nominal dollar risk constant.
* **Asymmetrical Trade Management:** A logic framework that blends high win-rate scalping with low win-rate/high-yield trend following. It secures early profits to eliminate risk on the trade, allowing the remaining position to run toward macro targets without psychological pressure.

### Institutional Price Action (SMC / ICT)
* **Smart Money Concepts (SMC):** A theoretical framework that attempts to reverse-engineer the algorithms used by central banks and massive institutional players, focusing on where liquidity (stop-losses) rests in the market.
* **Fair Value Gaps (FVG):** Price imbalances created by rapid, algorithmic buying or selling that leaves "gaps" in the price delivery. The lab's engines treat these as magnetic zones that price will eventually revisit to balance the books.
* **Order Blocks (OB):** The final accumulation of orders (often visualized as the last down-candle before a massive up-move) by large institutions before a markup phase. Used programmatically as high-probability invalidation levels (Stop Loss placement).
* **Optimal Trade Entry (OTE):** A specific, deep Fibonacci retracement zone (specifically the 79% level used in these scripts) that offers extreme discount pricing in a bullish trend, maximizing the mathematical Risk-to-Reward profile.
* **Multi-Timeframe Analysis (MTF):** The programmatic alignment of macro and micro data. The algorithms use 1-Hour data to determine the overarching structural bias and 15-Minute data to trigger surgical entries, preventing counter-trend executions.

### Prop-Firm Mechanics & Macro Indicators
* **Maximum Drawdown (Max DD):** The largest peak-to-trough drop in the equity curve. The lab utilizes this metric to ensure strategies survive the strict evaluation phases of proprietary trading firms.
* **Algorithmic News Embargo:** Hardcoded time filters that temporarily disable the trading engine during known high-impact macroeconomic data releases (e.g., CPI, FOMC at 10:00 AM and 2:00 PM EST) to avoid extreme slippage.
* **Yield Curve Spread (10Y-3M):** The difference between long-term and short-term US Treasury yields. An inverted curve is monitored as a leading indicator of liquidity contractions and economic recession.
* **Credit Stress Ratio (LQD/TLT):** A risk-on / risk-off gauge measuring the performance of Corporate Investment Grade bonds against safe-haven US Treasuries, indicating the market's underlying appetite for risk.

---

## Technologies Used

* **Python 3.x**
* **Pandas & NumPy**: High-performance data manipulation, vectorization, and signal logic processing.
* **YFinance**: Historical and live data extraction from Yahoo Finance.
* **Matplotlib**: Graphical engine utilized for plotting equity curves and visualizing maximum drawdown.

## How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/tiagocosta1234/macro-trading-lab.git](https://github.com/tiagocosta1234/macro-trading-lab.git)