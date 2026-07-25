"""
Portfolio Risk & Performance Analyzer
======================================
Pulls historical price data for a set of stocks, computes standard
risk and performance metrics, and generates a visual report.

Usage:
    python portfolio_analyzer.py

Edit the PORTFOLIO dictionary below to use your own tickers and weights.
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---------------------------------------------------------------------------
# 1. Adjusted Portfolio Analysis
# ---------------------------------------------------------------------------
PORTFOLIO = {
    "NVDA": 0.30,
    "JPM": 0.20,
    "JNJ":  0.20,
    "KO":  0.15,    
    "CROX":  0.15,   # 
}

START_DATE = "2021-01-01"
END_DATE = None          # None = through today
RISK_FREE_RATE = 0.045   # annualized, e.g. current ~T-bill yield
TRADING_DAYS = 252


# ---------------------------------------------------------------------------
# 2. DATA FETCHING
# ---------------------------------------------------------------------------
def fetch_price_data(tickers, start, end=None):
    """Download adjusted close prices for a list of tickers."""
    data = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = tickers
    return prices.dropna(how="all")


# ---------------------------------------------------------------------------
# 3. METRIC CALCULATIONS
# ---------------------------------------------------------------------------
def compute_returns(prices):
    """Daily simple returns for each asset."""
    return prices.pct_change().dropna()


def portfolio_returns(returns, weights):
    """Weighted daily return series for the whole portfolio."""
    w = np.array([weights[t] for t in returns.columns])
    return (returns * w).sum(axis=1)


def annualized_return(daily_returns, trading_days=TRADING_DAYS):
    total_growth = (1 + daily_returns).prod()
    n_years = len(daily_returns) / trading_days
    return total_growth ** (1 / n_years) - 1


def annualized_volatility(daily_returns, trading_days=TRADING_DAYS):
    return daily_returns.std() * np.sqrt(trading_days)


def sharpe_ratio(daily_returns, risk_free_rate=RISK_FREE_RATE, trading_days=TRADING_DAYS):
    excess_daily = daily_returns - (risk_free_rate / trading_days)
    return (excess_daily.mean() / daily_returns.std()) * np.sqrt(trading_days)


def max_drawdown(daily_returns):
    """Largest peak-to-trough decline in cumulative value."""
    cumulative = (1 + daily_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min(), drawdown


def historical_var(daily_returns, confidence=0.95):
    """Historical Value at Risk: worst expected daily loss at given confidence."""
    return -np.percentile(daily_returns, (1 - confidence) * 100)


def summarize_portfolio(returns, weights, risk_free_rate=RISK_FREE_RATE):
    """Build a one-row-per-metric summary table for the portfolio and each asset."""
    rows = {}

    port_ret = portfolio_returns(returns, weights)
    dd_val, _ = max_drawdown(port_ret)
    rows["Portfolio"] = {
        "Annual Return": annualized_return(port_ret),
        "Annual Volatility": annualized_volatility(port_ret),
        "Sharpe Ratio": sharpe_ratio(port_ret, risk_free_rate),
        "Max Drawdown": dd_val,
        "95% Daily VaR": historical_var(port_ret),
    }

    for ticker in returns.columns:
        r = returns[ticker]
        dd, _ = max_drawdown(r)
        rows[ticker] = {
            "Annual Return": annualized_return(r),
            "Annual Volatility": annualized_volatility(r),
            "Sharpe Ratio": sharpe_ratio(r, risk_free_rate),
            "Max Drawdown": dd,
            "95% Daily VaR": historical_var(r),
        }

    return pd.DataFrame(rows).T


# ---------------------------------------------------------------------------
# 4. VISUALIZATION
# ---------------------------------------------------------------------------
def plot_report(prices, returns, weights, summary, out_path="portfolio_report.png"):
    port_ret = portfolio_returns(returns, weights)
    cumulative = (1 + port_ret).cumprod()
    _, drawdown_series = max_drawdown(port_ret)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Portfolio Risk & Performance Report", fontsize=16, fontweight="bold")

    # Cumulative growth of $1
    ax = axes[0, 0]
    ax.plot(cumulative.index, cumulative.values, color="#2563eb", linewidth=1.8)
    ax.set_title("Growth of $1 Invested")
    ax.set_ylabel("Value ($)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(alpha=0.3)

    # Drawdown
    ax = axes[0, 1]
    ax.fill_between(drawdown_series.index, drawdown_series.values * 100, 0,
                     color="#dc2626", alpha=0.5)
    ax.set_title("Drawdown Over Time")
    ax.set_ylabel("Drawdown (%)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(alpha=0.3)

    # Correlation heatmap
    ax = axes[1, 0]
    corr = returns.corr()
    im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=8)
    ax.set_title("Asset Correlation Matrix")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # Risk/Return bar comparison
    ax = axes[1, 1]
    labels = summary.index
    x = np.arange(len(labels))
    width = 0.35
    ax.bar(x - width/2, summary["Annual Return"] * 100, width, label="Annual Return (%)", color="#16a34a")
    ax.bar(x + width/2, summary["Annual Volatility"] * 100, width, label="Annual Volatility (%)", color="#f59e0b")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_title("Return vs. Volatility by Asset")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(out_path, dpi=150)
    print(f"Saved report chart to {out_path}")


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------
def main():
    tickers = list(PORTFOLIO.keys())
    print(f"Fetching price history for: {', '.join(tickers)} ...")
    prices = fetch_price_data(tickers, START_DATE, END_DATE)
    returns = compute_returns(prices)

    summary = summarize_portfolio(returns, PORTFOLIO)

    pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
    print("\n=== Portfolio & Asset Metrics ===")
    print(summary.to_string())

    summary.to_csv("portfolio_summary.csv")
    print("\nSaved metrics to portfolio_summary.csv")

    plot_report(prices, returns, PORTFOLIO, summary)


if __name__ == "__main__":
    main()
