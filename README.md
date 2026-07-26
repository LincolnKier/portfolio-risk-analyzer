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

## Portfolio Strategy

This portfolio intentionally overweights **NVDA (30%)** as the primary
growth driver, reflecting conviction in AI/semiconductor demand. The
remaining 70% is diversified across established, low-correlation
sectors to offset that concentration risk:

- **NVDA (30%)** — semiconductors / AI growth
- **JPM (20%)** — financials
- **JNJ (20%)** — healthcare
- **KO (15%)** — consumer staples
- **CROX (15%)** — mid-cap consumer growth

The mix tests whether a single high-conviction growth bet can be
balanced by defensive, non-correlated holdings — exactly what the
correlation matrix and risk metrics below are built to measure.

## Findings

Running the analyzer on this portfolio produced:

| | Annual Return | Annual Volatility | Sharpe Ratio | Max Drawdown | 95% Daily VaR |
|---|---|---|---|---|---|
| **Portfolio** | 35.12% | 22.62% | 1.25 | -37.23% | 2.13% |
| NVDA | 64.77% | 50.97% | 1.14 | -66.34% | 4.68% |
| JPM | 23.68% | 24.23% | 0.81 | -38.77% | 2.34% |
| JNJ | 12.95% | 17.16% | 0.53 | -18.41% | 1.64% |
| KO | 11.61% | 16.31% | 0.48 | -17.27% | 1.55% |
| CROX | 15.21% | 54.92% | 0.45 | -73.86% | 4.56% |

**Diversification is doing real work here.** A volatility-weighted
average of the five holdings alone would put portfolio volatility
around 34% — the actual portfolio came in at 22.62%, roughly 11-12
points lower, because these five assets don't move in lockstep.

**Risk-adjusted return improved on every position except NVDA.** The
portfolio's Sharpe ratio (1.25) beats JPM, JNJ, KO, and CROX
individually, and comes close to NVDA's own 1.14 — meaning the blend
captured a large share of NVDA's growth while diversifying away much
of its risk.

**Drawdown protection is the clearest evidence.** Held alone, NVDA and
CROX would have produced drawdowns of -66% and -74% respectively. The
blended portfolio's worst drawdown was -37.23% — close to JPM's
individual number — showing that JNJ and KO acted as effective
ballast during downturns.

**Net result:** the portfolio captured roughly half of NVDA's raw
return (35% vs. 65%) while cutting volatility nearly in half and
drawdown risk by almost half compared to holding either growth stock
on its own — a textbook demonstration of diversification improving
risk-adjusted returns without simply diluting them away.

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
