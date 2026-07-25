# Portfolio Risk & Performance Analyzer

A Python tool that pulls historical stock price data and computes the
risk and performance metrics used in quantitative finance and actuarial
risk analysis: annualized return, volatility, Sharpe ratio, maximum
drawdown, Value at Risk (VaR), and inter-asset correlation.

## What it does

Given a portfolio (a set of tickers and their weights), the tool:

1. Downloads historical adjusted-close prices via the `yfinance` library.
2. Computes daily and annualized returns for each asset and for the
   portfolio as a whole.
3. Calculates key risk metrics:
   - **Annualized Return** — compounded average yearly growth
   - **Annualized Volatility** — standard deviation of returns, annualized
   - **Sharpe Ratio** — risk-adjusted return relative to a risk-free rate
   - **Maximum Drawdown** — largest peak-to-trough decline
   - **95% Historical VaR** — the daily loss threshold exceeded only 5% of the time
4. Generates a single PNG report with four panels: cumulative growth,
   drawdown over time, an asset correlation heatmap, and a return-vs-volatility
   comparison bar chart.
5. Exports a CSV of all computed metrics.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Edit the `PORTFOLIO` dictionary at the top of `portfolio_analyzer.py` with
your own tickers and weights (must sum to 1.0), then run:

```bash
python portfolio_analyzer.py
```

This produces:
- `portfolio_report.png` — the visual report
- `portfolio_summary.csv` — the metrics table

## Example output

Default portfolio: AAPL, MSFT, JNJ, JPM, and VTI (a broad-market ETF as
a diversifier), each with a set weight.

## Why this project

This was built to demonstrate applied quantitative risk analysis —
the same core concepts (volatility, drawdown, VaR, diversification)
that show up in actuarial and financial risk work, implemented as a
clean, reproducible Python tool rather than a one-off spreadsheet.

## Possible extensions

- Add a Monte Carlo simulation for forward-looking VaR
- Add an efficient frontier optimizer (find the weight mix that
  maximizes Sharpe ratio)
- Compare portfolio performance against a benchmark index (e.g., S&P 500)
- Wrap it in a simple Streamlit dashboard for interactive weight adjustment
