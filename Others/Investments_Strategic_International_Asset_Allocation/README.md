# Strategic International Asset Allocation using Currency Hedging and Predictive Signals

### Context:
Course Project for **FIN-405: Investments** at **EPFL**, Master in Financial Engineering Course. An empirical study of international diversification, momentum, and macro-finance factors, using monthly data (2000-2024) across seven major markets (Australia, France, Germany, Japan, Switzerland, UK, USA).

---

## Key Takeaways:
1. **Plain Diversification Beats Clever Signals**: The DIV portfolios consistently outperform momentum, reversal, carry, and dollar strategies on a risk-adjusted basis.
2. **Currency Hedging is a Volatility Tool, Not a Return Enhancer**: It smooths returns but costs you when the foreign currency is strengthening.
3. **Momentum and Reversal Signals Don't Pay Off Here**: Long legs look promising, but losses on the short side wash out any net edge.
4. **Stacking Strategies Doesn't Guarantee a Better Fund**: A risk-parity overlay of the signal strategies fails to improve on a simple T-Bill/diversified-portfolio blend.
5. **Market Risk Still Explains Most of the Returns**: A Fama-French factor analysis confirms the fund is primarily a market-risk play, with only modest evidence of additional factor exposure.

---

## Tools Used:
- **Data**: WRDS (country equity returns), FRED (FX rates, interbank rates)
- **Analysis**: Python (pandas, statsmodels/OLS regressions, portfolio construction)
- **Report**: LaTeX

---

## Overview
The project builds and analyzes six strategies on hedged/unhedged international equity and currency exposures:
- **DIV**: Equally-Weighted, Risk-Parity, and Mean-Variance diversified portfolios (hedged & unhedged).
- **MOM**: 12-month equity index momentum (long-short, ranked).
- **REV**: 5-year equity index long-term reversal (long-short, ranked).
- **CARRY**: Currency carry trade based on interbank rate differentials.
- **DOLLAR**: Long basket of foreign currencies vs. USD.

These are then combined into a **STRAT** risk-parity overlay (MOM, REV, CARRY, DOLLAR) and optimized alongside DIV and T-Bills into a final **FUND** strategy targeting 15% annualized volatility, with performance assessed against the Fama-French five-factor model and interpreted through EMH, CAPM, and APT.

---

## Repository Structure
```
FIN405_Strategic_International_Asset_Allocation/
├── README.md
├── FIN405_Strategic_Asset_Allocation_Report.pdf
└── code/                          # Python scripts/notebooks for data processing and strategy construction
```