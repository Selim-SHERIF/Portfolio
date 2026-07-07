# NOTE: This script was automatically exported from a Jupyter Notebook (.ipynb).
# It is not designed for direct execution as a standalone Python script, but is
# provided for convenience.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import minimize
from scipy import stats
import statsmodels.api as sm
import seaborn as sns


# %% [markdown]
# ### Reading monthly returns
# 
# Monthly figures, we have end-of-month data, not always prefectly aligned to the end of month

# %%
USD_monthly_returns = pd.read_csv('data/US_value_weighted_returns.csv', parse_dates=['date'], index_col='date')

japan       = pd.read_csv("data/JAPAN.csv",       parse_dates=["date"], index_col="date")[["mportret"]]
australia   = pd.read_csv("data/AUSTRALIA.csv",   parse_dates=["date"], index_col="date")[["mportret"]]
germany     = pd.read_csv("data/GERMANY.csv",     parse_dates=["date"], index_col="date")[["mportret"]]
france      = pd.read_csv("data/FRANCE.csv",      parse_dates=["date"], index_col="date")[["mportret"]]
switzerland = pd.read_csv("data/SWITZERLAND.csv", parse_dates=["date"], index_col="date")[["mportret"]]
unitedkingdom = pd.read_csv("data/UNITEDKINGDOM.csv", parse_dates=["date"], index_col="date")[["mportret"]]

switzerland.head()

# %% [markdown]
# ### Reading exchange rates

# %% [markdown]
# Monthly figures, we have beginning-of-month data

# %%
def load_fx_series(filepath: str, invert: bool = False) -> pd.Series:
    """Load FX series and convert to currency → USD if needed."""
    df = pd.read_csv(filepath, parse_dates=['observation_date'], index_col='observation_date')
    series = df.iloc[:, 0]
    return 1 / series if invert else series

# Load FX rates (all to USD)
fx_jpy = load_fx_series('data/EXJPUS.csv', invert=True)   # JPY → USD
fx_chf = load_fx_series('data/EXSZUS.csv', invert=True)   # CHF → USD
fx_aud = load_fx_series('data/EXUSAL.csv')                # AUD → USD
fx_eur = load_fx_series('data/EXUSEU.csv')                # EUR → USD
fx_gbp = load_fx_series('data/EXUSUK.csv')                # GBP → USD

# Preview one of the results
fx_chf.tail()
fx_jpy.tail()
fx_gbp.tail()

# %% [markdown]
# FX are beginning of month, returns are end of months --> we will shift back FX to previous month, we will also push returns to exactly end of month.

# %%
def align_returns_to_month_end(ret_df: pd.DataFrame) -> pd.DataFrame:
    """
    Take a returns DataFrame (or Series) whose index is a date somewhere
    in a month, and “snap” that date to the LAST calendar day of the same month.

    E.g. 2000-04-28 → 2000-04-30; 2000-02-29 → 2000-02-29; 2000-06-30 → 2000-06-30.
    """
    df = ret_df.copy()
    df.index = df.index.to_period("M").to_timestamp("M")
    return df

def align_fx_to_previous_month_end(fx_obj) -> pd.DataFrame:
    """
    Take an FX Series or single‐column DataFrame whose index is ANY date 
    in a month (e.g. 2000-05-01 or 2000-05-15), and move that entire index 
    to the *previous* month’s last calendar day.

    - If fx_obj.index is a DatetimeIndex:  (ix.to_period("M") - 1).to_timestamp("M")
    - If fx_obj.index is already a PeriodIndex:        (ix - 1).to_timestamp("M")
    """
    # Copy it so we do not mutate the original
    df = fx_obj.copy()
    ix = df.index

    if isinstance(ix, pd.DatetimeIndex):
        df.index = (ix.to_period("M") - 1).to_timestamp("M")

    elif isinstance(ix, pd.PeriodIndex):
        df.index = (ix - 1).to_timestamp("M")

    else:
        dt = pd.to_datetime(ix)
        df.index = (dt.to_period("M") - 1).to_timestamp("M")

    return df

# %%
def merge_one_country(returns_df: pd.DataFrame, fx_obj) -> pd.DataFrame:
    """
    1) Snap returns_df index to the SAME month‐end.
    2) Snap fx_obj (Series or DataFrame) index to the PREVIOUS month‐end.
    3) Rename columns to 'return' and 'fx'.
    4) Merge on that common index (inner join).
    """
    # --- Step 1: Align returns to month‐end (same month).
    ret_aligned = align_returns_to_month_end(returns_df)
    ret_aligned = ret_aligned.rename(columns={ret_aligned.columns[0]: "return"})
    
    # --- Step 2: Align FX backward to previous month‐end.
    fx_aligned = align_fx_to_previous_month_end(fx_obj)
    
    # If fx_aligned is a Series, convert it to a DataFrame named "fx".
    if isinstance(fx_aligned, pd.Series):
        fx_aligned = fx_aligned.to_frame(name="fx")
    else:
        # Otherwise it's already a DataFrame with one column—rename that column to "fx"
        fx_aligned = fx_aligned.rename(columns={fx_aligned.columns[0]: "fx"})
    
    # --- Step 3: Inner‐merge on the aligned index.
    merged = pd.merge(
        ret_aligned,
        fx_aligned,
        left_index=True,
        right_index=True,
        how="inner"
    )
    return merged



# %%
returns_dict = {
    "japan":       japan,
    "australia":   australia,
    "germany":     germany,
    "france":      france,
    "switzerland": switzerland,
    "unitedkingdom": unitedkingdom
}

fx_dict = {
    "japan":         fx_jpy,   
    "switzerland":   fx_chf,   
    "australia":     fx_aud,   
    "germany":       fx_eur,   
    "france":        fx_eur,   
    "unitedkingdom": fx_gbp    
}

merged_data = {}

for country in returns_dict.keys():
    # grab raw returns DataFrame + raw FX (Series or DF) for this country
    raw_ret = returns_dict[country]
    raw_fx  = fx_dict[country]

    merged_df = merge_one_country(raw_ret, raw_fx)
    merged_data[country] = merged_df


for country in merged_data.keys():
    merged_data[country] = merged_data[country][merged_data[country].index >= '2002-01-01']


# %%
merged_data["japan"].head()

# %% [markdown]
# # 3.a. Returns of each index in USD

# %%
def compute_usd_returns(merged_data: dict) -> dict:
    """
    Given:
      - merged_data: a dict mapping country_name → DataFrame
        where each DataFrame has exactly two columns:
           'return' (local index return, aligned to month‐end)
           'fx'     (USD exchange rate, aligned to previous month‐end)
    
    This function:
      1. Copies each country’s DataFrame.
      2. Computes fx_return = fx / fx.shift(1) - 1
      3. Computes usd_return = (1 + return) * (1 + fx_return) - 1
      4. Drops any rows with NaNs (from the shift).
      5. Returns a new dict (same keys) whose DataFrames now contain:
         ['return', 'fx', 'fx_return', 'usd_return'].
    """
    processed_data = {}
    
    for country, df_original in merged_data.items():
        # 1) Make a copy so we don’t overwrite the original
        df = df_original.copy()
        
        # 2) Compute the monthly FX return
        #    (percent change in the USD/FX rate from previous row → current row)
        df['fx_return'] = df['fx'] / df['fx'].shift(1) - 1
        
        # 3) Compute the USD‐denominated total return:
        #    (1 + local_index_return) * (1 + fx_return) − 1
        df['usd_return'] = (1 + df['return']) * (1 + df['fx_return']) - 1
        
        # 4) Drop any rows with NaNs (the first row will become NaN in fx_return)
        df.dropna(inplace=True)
        
        # 5) Store the result under the same country key
        processed_data[country] = df
    
    return processed_data

# %%
processed_data = compute_usd_returns(merged_data)
processed_data["switzerland"].head(10)

# %% [markdown]
# # 3.b. Currency-hedged index return

# %% [markdown]
# Initializing correct data, start with interbank rates

# %%
#    Read each 3-month interbank CSV, parse the "observation_date" column as DatetimeIndex,
#    select only the rate column, and rename it to the correct ISO code.

aus_ib = pd.read_csv(
    "data/AUSTRALIA_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
aus_ib = aus_ib.iloc[:, [0]].rename(columns={aus_ib.columns[0]: "AUD"})
aus_ib["AUD"] = aus_ib["AUD"] / 100


eur_ib = pd.read_csv(
    "data/EUROPE_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
eur_ib = eur_ib.iloc[:, [0]].rename(columns={eur_ib.columns[0]: "EUR"})
eur_ib["EUR"] = eur_ib["EUR"] / 100


gbp_ib = pd.read_csv(
    "data/GREATBRITAIN_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
gbp_ib = gbp_ib.iloc[:, [0]].rename(columns={gbp_ib.columns[0]: "GBP"})
gbp_ib["GBP"] = gbp_ib["GBP"] / 100


jpy_ib = pd.read_csv(
    "data/JAPAN_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
jpy_ib = jpy_ib.iloc[:, [0]].rename(columns={jpy_ib.columns[0]: "JPY"})
jpy_ib["JPY"] = jpy_ib["JPY"] / 100


chf_ib = pd.read_csv(
    "data/SWITZERLAND_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
chf_ib = chf_ib.iloc[:, [0]].rename(columns={chf_ib.columns[0]: "CHF"})
chf_ib["CHF"] = chf_ib["CHF"] / 100

usd_ib = pd.read_csv(
    "data/USA_IB.csv",
    parse_dates=["observation_date"],
    index_col="observation_date"
)
usd_ib = usd_ib.iloc[:, [0]].rename(columns={usd_ib.columns[0]: "USD"})
usd_ib["USD"] = usd_ib["USD"] / 100

# Combine all six DataFrames side-by-side (inner join on the common dates)
ibexr = pd.concat(
    [usd_ib, eur_ib, jpy_ib, gbp_ib, chf_ib, aus_ib],
    axis=1,
    join="inner"
)

# Ensure the index is sorted and is exactly at month-end
ibexr.index = pd.to_datetime(ibexr.index)
ibexr = ibexr.sort_index()

ibexr = ibexr.resample("M").last().dropna(how="all")

print(ibexr.head())


# %%
iso_map = {
    "japan":         "JPN",
    "australia":     "AUS",
    "germany":       "DEU",
    "france":        "FRA",
    "switzerland":   "CHE",
    "unitedkingdom": "GBR"
}

idx_returns = pd.DataFrame({
    iso_map[country]: df["usd_return"]
    for country, df in processed_data.items()
})
idx_returns.index = pd.to_datetime(idx_returns.index)
idx_returns = idx_returns.sort_index()

cexr = pd.DataFrame({
    "JPY": processed_data["japan"]["fx"],
    "CHF": processed_data["switzerland"]["fx"],
    "AUD": processed_data["australia"]["fx"],
    "EUR": processed_data["germany"]["fx"],
    "GBP": processed_data["unitedkingdom"]["fx"]
})
cexr.index = pd.to_datetime(cexr.index)
cexr = cexr.sort_index()

idx_returns.head()

# %%
ibexr.to_csv("data/ibexr.csv")
idx_returns.to_csv("data/idx_returns.csv")
cexr.to_csv("data/cexr.csv")

# %% [markdown]
# ## New implementation of currency hedging

# %%
# From now on, we truncate dataframes to all start from 2002-04
ibexr = ibexr[ibexr.index >= '2002-04']
cexr = cexr[cexr.index >= '2002-04']
idx_returns = idx_returns[idx_returns.index >= '2002-04']

# Convert annual interbank rates to monthly by dividing by 12
ibexr_monthly = ibexr / 12

# Create the country-currency mapping based on your data
country_currency_map = {
    'JPN': 'JPY',
    'AUS': 'AUD', 
    'DEU': 'EUR',
    'FRA': 'EUR',
    'CHE': 'CHF',
    'GBR': 'GBP'
}

# Initialize DataFrames for results
excess_return_currency_in_USD = pd.DataFrame(index=ibexr_monthly.index)
currency_hedged_index_return = pd.DataFrame(index=excess_return_currency_in_USD.index)

# Calculate currency hedged returns for each country
for country, currency in country_currency_map.items():
    fact = cexr[currency] / cexr[currency].shift(1)
    foreign_rate = ibexr_monthly[currency]  # Use currency column from ibexr
    us_rate = ibexr_monthly['USD']
    X = fact * (1 + foreign_rate) - (1 + us_rate)
    excess_return_currency_in_USD[country + '_currency_excess_return'] = X
    currency_hedged_index_return[country + '_currency_hedged_return'] = idx_returns[country] - X

excess_return_currency_in_USD.dropna(inplace=True)
currency_hedged_index_return.dropna(inplace=True)

# Display results
print("Currency Excess Returns in USD:")
print(excess_return_currency_in_USD.head())
print("\nCurrency Hedged Index Returns:")
print(currency_hedged_index_return.head())

# %%
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
axes = axes.flatten()

countries = ['JPN', 'AUS', 'DEU', 'FRA', 'CHE', 'GBR']

for i, country in enumerate(countries):
    # Cumulative returns
    unhedged_cum = (1 + idx_returns[country]).cumprod()
    hedged_cum = (1 + currency_hedged_index_return[country + '_currency_hedged_return']).cumprod()
    
    axes[i].plot(unhedged_cum, label='Unhedged', alpha=0.8)
    axes[i].plot(hedged_cum, label='Hedged', alpha=0.8)
    axes[i].set_title(country)
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# Step 1: Check one country in detail - let's use JPN
print("=== DEBUGGING JPN CURRENCY HEDGING ===")
country = 'JPN'
currency = 'JPY'

# Check the data alignment first
print(f"\n1. Data ranges:")
print(f"cexr range: {cexr.index.min()} to {cexr.index.max()}")
print(f"ibexr range: {ibexr_monthly.index.min()} to {ibexr_monthly.index.max()}")
print(f"idx_returns range: {idx_returns.index.min()} to {idx_returns.index.max()}")

# Pick a specific date to trace through
test_date_idx = 10
test_date = cexr.index[test_date_idx]
print(f"\n2. Testing date: {test_date}")

# Check FX data
fx_current = cexr[currency].iloc[test_date_idx]
fx_previous = cexr[currency].iloc[test_date_idx-1] 
fact = fx_current / fx_previous
print(f"FX current: {fx_current:.6f}")
print(f"FX previous: {fx_previous:.6f}")
print(f"FX factor (St+1/St): {fact:.6f}")

# Check interest rates
foreign_rate = ibexr_monthly[currency].iloc[test_date_idx]
us_rate = ibexr_monthly['USD'].iloc[test_date_idx]
print(f"Foreign rate (monthly): {foreign_rate:.6f}")
print(f"US rate (monthly): {us_rate:.6f}")

# Calculate X step by step
term1 = fact * (1 + foreign_rate)
term2 = (1 + us_rate)
X = term1 - term2
print(f"\n3. Currency excess return calculation:")
print(f"fact * (1 + foreign_rate) = {fact:.6f} * {1 + foreign_rate:.6f} = {term1:.6f}")
print(f"(1 + us_rate) = {term2:.6f}")
print(f"X = {term1:.6f} - {term2:.6f} = {X:.6f}")

# Check the original return
original_return = idx_returns[country].iloc[test_date_idx]
hedged_return = original_return - X
print(f"\n4. Final calculation:")
print(f"Original return: {original_return:.6f}")
print(f"Currency excess return (X): {X:.6f}")
print(f"Hedged return: {original_return:.6f} - {X:.6f} = {hedged_return:.6f}")

# Sanity check: if JPY strengthens, US investor should benefit from unhedged
if fact > 1:
    print(f"\n5. Sanity check: JPY strengthened (factor > 1)")
    print(f"   Unhedged should be BETTER than hedged")
    print(f"   Unhedged: {original_return:.6f}, Hedged: {hedged_return:.6f}")
else:
    print(f"\n5. Sanity check: JPY weakened (factor < 1)")  
    print(f"   Hedged should be BETTER than unhedged")
    print(f"   Unhedged: {original_return:.6f}, Hedged: {hedged_return:.6f}")

# %% [markdown]
# # 3.c. Diversification 

# %%
# Calculate equally weighted portfolio returns
portfolio_unhedged = idx_returns.mean(axis=1)
portfolio_hedged = currency_hedged_index_return.mean(axis=1)

# Plot cumulative returns
plt.figure(figsize=(10, 6))
(1 + portfolio_unhedged).cumprod().plot(label='Unhedged Portfolio', color='red', alpha=0.8)
(1 + portfolio_hedged).cumprod().plot(label='Hedged Portfolio', color='blue', alpha=0.8)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.title('Equally Weighted Portfolio: Hedged vs Unhedged')
plt.grid(True, alpha=0.3)
plt.show()

# %%
# Risk Parity function
def risk_parity_strategy(returns_df, window=60):
    vol_rolling = returns_df.rolling(window=window, min_periods=window).std()
    inv_vol = 1.0 / vol_rolling
    inv_vol.replace([np.inf, -np.inf], np.nan, inplace=True)
    total_inv_vol = inv_vol.sum(axis=1)
    weights = inv_vol.div(total_inv_vol, axis=0)
    lagged_weights = weights.shift(1)
    portfolio_rets = (lagged_weights * returns_df).sum(axis=1)
    return portfolio_rets, weights

# Calculate risk parity returns
rp_unhedged, weights_unhedged = risk_parity_strategy(idx_returns)
rp_hedged, weights_hedged = risk_parity_strategy(currency_hedged_index_return)

# Remove first 5 years
rp_unhedged = rp_unhedged[rp_unhedged.index >= '2007-05']
rp_hedged = rp_hedged[rp_hedged.index >= '2007-05']

# Plot cumulative returns
plt.figure(figsize=(10, 6))
(1 + rp_unhedged).cumprod().plot(label='Unhedged RP', color='red', alpha=0.8)
(1 + rp_hedged).cumprod().plot(label='Hedged RP', color='blue', alpha=0.8)
plt.legend()
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.title('Risk Parity Strategy: Hedged vs Unhedged')
plt.grid(True, alpha=0.3)
plt.show()

# %%
# Markowitz Portfolio Optimizer
def markowitz_solver(sigma_matrix, mu_vector, risk_free, risk_aversion=1):
    asset_count = len(mu_vector)
    
    # Utility maximization: maximize expected return - (risk_aversion/2) * variance
    utility_func = lambda weights: -(np.dot(mu_vector - risk_free*np.ones(asset_count), weights) - 
                                   0.5 * risk_aversion * np.dot(weights.T, np.dot(sigma_matrix, weights)))
    
    # Portfolio weights must sum to 1
    budget_constraint = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]
    
    # Equal weight starting point
    initial_guess = np.ones(asset_count) / asset_count
    
    # Long-only constraints (no shorting)
    weight_bounds = [(0, 1) for _ in range(asset_count)]
    
    solution = minimize(utility_func, initial_guess, method='SLSQP', 
                       bounds=weight_bounds, constraints=budget_constraint)
    
    return solution.x

def rolling_portfolio_optimizer(asset_returns):
    # Calculate rolling statistics
    rolling_means = asset_returns.rolling(window=60).mean()
    rolling_covariances = asset_returns.rolling(window=60).cov().bfill()
    
    # Get risk-free rate data
    treasury_rates = ibexr_monthly.loc[:, ['USD']]
    treasury_rates.index = pd.to_datetime(treasury_rates.index)
    
    # Find overlapping time periods
    shared_periods = asset_returns.index.intersection(treasury_rates.index)
    rf_rates = treasury_rates.loc[shared_periods].values.flatten()
    
    # Filter data to shared periods
    filtered_returns = asset_returns.loc[shared_periods]
    filtered_means = rolling_means.loc[shared_periods]
    filtered_covs = rolling_covariances.loc[shared_periods]
    
    # Initialize weight container
    weight_history = []
    
    # Fill initial periods with equal weights
    n_assets = len(asset_returns.columns)
    warmup_period = 60
    
    for period in range(warmup_period):
        weight_history.append(np.ones(n_assets) / n_assets)
    
    # Optimize for each period after warmup
    optimization_periods = len(filtered_means) - warmup_period
    
    for t in range(optimization_periods):
        period_idx = t + warmup_period
        
        # Extract period statistics
        period_means = filtered_means.iloc[period_idx].values
        
        # Get covariance matrix for this period
        cov_start = period_idx
        cov_end = period_idx + n_assets
        period_cov = filtered_covs.iloc[cov_start:cov_end].values.reshape(n_assets, n_assets)
        
        # Optimize portfolio
        optimal_weights = markowitz_solver(period_cov, period_means, rf_rates[period_idx])
        weight_history.append(optimal_weights)
    
    # Create weights dataframe
    weights_df = pd.DataFrame(weight_history, index=shared_periods, columns=asset_returns.columns)
    
    # Normalize weights (defensive programming)
    weights_df = weights_df.div(weights_df.sum(axis=1), axis=0)
    
    return weights_df

def portfolio_backtest(returns_data, allocation_weights):
    # Synchronize data
    overlap_dates = returns_data.index.intersection(allocation_weights.index)
    synced_returns = returns_data.loc[overlap_dates]
    synced_weights = allocation_weights.loc[overlap_dates]
    
    # Use lagged weights (realistic implementation)
    lagged_allocations = synced_weights.shift(1)
    
    # Compute weighted portfolio returns
    portfolio_performance = (lagged_allocations * synced_returns).sum(axis=1)
    
    return portfolio_performance.dropna()

# Execute optimization for both strategies
print("Computing unhedged Markowitz portfolio...")
unhedged_allocations = rolling_portfolio_optimizer(idx_returns)
unhedged_performance = portfolio_backtest(idx_returns, unhedged_allocations)

print("Computing hedged Markowitz portfolio...")
hedged_allocations = rolling_portfolio_optimizer(currency_hedged_index_return)
hedged_performance = portfolio_backtest(currency_hedged_index_return, hedged_allocations)

# Apply lookback filter (remove initial years)
unhedged_performance = unhedged_performance[unhedged_performance.index >= '2007-05']
hedged_performance = hedged_performance[hedged_performance.index >= '2007-05']

# Visualization
plt.figure(figsize=(12, 7))
wealth_unhedged = (1 + unhedged_performance).cumprod()
wealth_hedged = (1 + hedged_performance).cumprod()

wealth_unhedged.plot(label='Unhedged Markowitz', color='crimson', linewidth=2, alpha=0.9)
wealth_hedged.plot(label='Hedged Markowitz', color='navy', linewidth=2, alpha=0.9)

plt.legend(fontsize=12)
plt.xlabel('Time Period', fontsize=11)
plt.ylabel('Wealth Index', fontsize=11)
plt.title('Markowitz Mean-Variance Optimization: Currency Impact Analysis', fontsize=13)
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()

print(f"Unhedged final wealth: {wealth_unhedged.iloc[-1]:.3f}")
print(f"Hedged final wealth: {wealth_hedged.iloc[-1]:.3f}")

# %% [markdown]
# ## Performance analysis

# %%
# Performance comparison function
def portfolio_performance_SR(returns, risk_free_rate):
    mean = (returns.mean()) * 12
    standard_dev = (returns.std()) * np.sqrt(12)
    SR = (mean - risk_free_rate.mean()) / standard_dev
    return mean, standard_dev, SR

# Create comparison dataframe using all our strategies
comparative_df = pd.DataFrame.from_dict({
    'Unhedged EW': portfolio_performance_SR(portfolio_unhedged, ibexr_monthly['USD']),
    'Hedged EW': portfolio_performance_SR(portfolio_hedged, ibexr_monthly['USD']),
    'Unhedged RP': portfolio_performance_SR(rp_unhedged, ibexr_monthly['USD']),
    'Hedged RP': portfolio_performance_SR(rp_hedged, ibexr_monthly['USD']),
    'Unhedged MVO': portfolio_performance_SR(unhedged_performance, ibexr_monthly['USD']),
    'Hedged MVO': portfolio_performance_SR(hedged_performance, ibexr_monthly['USD'])
}, orient='index', columns=['Mean', 'Volatility', 'Sharpe Ratio'])

print("Portfolio Performance Comparison:")
print("=" * 50)
print(comparative_df.round(4))

# %% [markdown]
# ## **Question 4: Equity Index Momentum Strategy (MOM)**

# %%
def compute_momentum_returns(hedged_returns: pd.DataFrame, return_weights: bool = False):
    """
    Compute monthly returns of a long-short momentum strategy,
    and optionally return the weight matrix used to construct the portfolio.

    Parameters:
    -----------
    hedged_returns : pd.DataFrame
        Currency-hedged index returns.
    
    return_weights : bool
        If True, also return the full weight matrix.

    Returns:
    --------
    mom_returns : pd.Series
        Monthly momentum strategy returns.
    
    mom_weights : pd.DataFrame (optional)
        Weights applied to each index each month (if return_weights is True).
    """
    # 1. Compute lagged 11-month cumulative return
    signal = (1 + hedged_returns).rolling(window=11).apply(np.prod, raw=True) - 1
    signal = signal.shift(1)

    # 2. Rank each row
    ranks = signal.rank(axis=1, method="first")

    # 3. Centered weights
    N = hedged_returns.shape[1]
    center = (N + 1) / 2
    raw_weights = ranks.subtract(center, axis=0)

    # Step 4: Normalize weights to sum long = +1, short = –1
    def normalize_row(row):
        pos_sum = row[row > 0].sum()
        neg_sum = row[row < 0].sum()

        # Scale positive weights to sum to +1, negatives to sum to -1
        norm_row = row.copy()
        if pos_sum != 0:
            norm_row[row > 0] /= pos_sum
        if neg_sum != 0:
            norm_row[row < 0] /= -neg_sum  # use minus to make it negative
        return norm_row


    mom_weights = raw_weights.apply(normalize_row, axis=1)

    # 5. Compute returns
    mom_returns = (mom_weights * hedged_returns).sum(axis=1)
    mom_returns.name = "MOM"

    return (mom_returns, mom_weights) if return_weights else mom_returns

def analyze_long_short_strategy(name: str, hedged_returns: pd.DataFrame,
                                weights: pd.DataFrame, total_returns: pd.Series):
    """
    General analyzer for any long-short strategy (momentum, reversal, carry, etc.).

    Parameters:
    -----------
    name : str
        Strategy name for printing (e.g., "Momentum Strategy").

    hedged_returns : pd.DataFrame
        Currency-hedged excess returns for each index (rows = time, cols = assets).

    weights : pd.DataFrame
        Strategy weights (rows = time, cols = assets). Normalized: long sum = +1, short sum = -1.

    total_returns : pd.Series
        Realized total strategy return time series (weights * returns).

    Returns:
    --------
    Dict with annualized mean, std, Sharpe, t-stat, and p-value for:
        - long leg
        - short leg
        - total strategy
    """
    # Filter active months (non-zero exposure)
    active_mask = weights.abs().sum(axis=1) > 0
    weights = weights.loc[active_mask]
    hedged_returns = hedged_returns.loc[active_mask]
    total_returns = total_returns.loc[active_mask]

    # Split into long and short weights
    long_weights = weights.where(weights > 0, 0)
    short_weights = weights.where(weights < 0, 0)

    # Compute leg returns
    long_returns = (long_weights * hedged_returns).sum(axis=1)
    short_returns = (short_weights * hedged_returns).sum(axis=1)

    def summarize(x: pd.Series, label: str):
        mean_m = x.mean()
        std_m = x.std()
        sharpe_m = mean_m / std_m if std_m != 0 else 0

        mean_a = mean_m * 12
        std_a = std_m * np.sqrt(12)
        sharpe_a = sharpe_m * np.sqrt(12)

        t_stat, p_val = stats.ttest_1samp(x.dropna(), popmean=0)

        print(f"\n{name} — {label} Performance")
        print(f"Annualized Mean Return : {mean_a:.5f}")
        print(f"Annualized Std Dev     : {std_a:.5f}")
        print(f"Annualized Sharpe Ratio: {sharpe_a:.2f}")
        print(f"T-statistic             : {t_stat:.2f}, p-value = {p_val:.4f}")

        return {
            "mean_annual": mean_a,
            "std_annual": std_a,
            "sharpe_annual": sharpe_a,
            "t_stat": t_stat,
            "p_value": p_val
        }

    results = {
        "long": summarize(long_returns, "Long Leg"),
        "short": summarize(short_returns, "Short Leg"),
        "total": summarize(total_returns, "Total Strategy")
    }

    return results



# %%
# Get both return series and weights for Q4.b
mom_returns, mom_weights = compute_momentum_returns(currency_hedged_index_return, return_weights=True)
results_mom = analyze_long_short_strategy("Momentum", currency_hedged_index_return,
                                          mom_weights, mom_returns)

# %%
div_returns = rp_hedged
active_mask = mom_weights.abs().sum(axis=1) > 0

# Apply to both series
mom_returns_filtered = mom_returns.loc[active_mask]
div_returns_filtered = div_returns.loc[active_mask]

# Align the two series
reg_df = pd.concat([mom_returns_filtered, div_returns_filtered], axis=1).dropna()
reg_df.columns = ['MOM', 'DIV']

# OLS Regression
X = sm.add_constant(reg_df['DIV'])
y = reg_df['MOM']
model = sm.OLS(y, X).fit()

print(model.summary())

# %% [markdown]
# ## **Question 5: Equity Index Long Term Reversal strategy (REV)**

# %%
def compute_reversal_returns(hedged_returns: pd.DataFrame, return_weights: bool = False):
    """
    Compute monthly returns of a long-short reversal strategy (REV),
    and optionally return the weight matrix.

    Parameters:
    -----------
    hedged_returns : pd.DataFrame
        Currency-hedged index returns (monthly, columns = ISO codes).

    return_weights : bool
        If True, also return the weight matrix.

    Returns:
    --------
    rev_returns : pd.Series
        Monthly returns of the reversal strategy.

    rev_weights : pd.DataFrame (optional)
        The long-short weights applied each month.
    """
    # Step 1: Compute 5-year cumulative return from t-60 to t-12
    past_5y = (1 + hedged_returns).rolling(window=48).apply(np.prod, raw=True) - 1
    past_5y = past_5y.shift(12)  # lag to end at t-12

    # Step 2: Rank past returns across countries
    ranks = past_5y.rank(axis=1, method="first")

    # Step 3: Centered reversal weights: w_i = (N + 1)/2 − Rank_i
    N = hedged_returns.shape[1]
    center = (N + 1) / 2
    raw_weights = center - ranks

    # Step 4: Normalize weights to sum long = +1, short = –1
    def normalize_row(row):
        pos_sum = row[row > 0].sum()
        neg_sum = row[row < 0].sum()

        # Scale positive weights to sum to +1, negatives to sum to -1
        norm_row = row.copy()
        if pos_sum != 0:
            norm_row[row > 0] /= pos_sum
        if neg_sum != 0:
            norm_row[row < 0] /= -neg_sum  # use minus to make it negative
        return norm_row


    rev_weights = raw_weights.apply(normalize_row, axis=1)

    # Step 5: Compute monthly portfolio return
    rev_returns = (rev_weights * hedged_returns).sum(axis=1)
    rev_returns.name = "REV"

    return (rev_returns, rev_weights) if return_weights else rev_returns



# %%
rev_returns, rev_weights = compute_reversal_returns(currency_hedged_index_return, return_weights=True)
results_rev = analyze_long_short_strategy("Reversal", currency_hedged_index_return,
                                          rev_weights, rev_returns)

# %%

# Step 1: Get active months
active_mask = rev_weights.abs().sum(axis=1) > 0

# Step 2: Apply mask to both REV and DIV
rev_returns_filtered = rev_returns.loc[active_mask]
div_returns_filtered = rp_hedged.loc[active_mask]

# Step 3: Align the two series
reg_df_rev = pd.concat([rev_returns_filtered, div_returns_filtered], axis=1).dropna()
reg_df_rev.columns = ['REV', 'DIV']

# Step 4: Run regression
X = sm.add_constant(reg_df_rev['DIV'])
y = reg_df_rev['REV']
model_rev = sm.OLS(y, X).fit()

print(model_rev.summary())


# %%
# === Step 0: Align all strategies to common index and active months ===
common_idx = mom_returns.index.intersection(rev_returns.index).intersection(rp_hedged.index)
mom = mom_returns.loc[common_idx]
rev = rev_returns.loc[common_idx]
div = rp_hedged.loc[common_idx]

# Align full returns for weighted calculation
returns = currency_hedged_index_return.loc[common_idx]
mom_weights = mom_weights.loc[common_idx]
rev_weights = rev_weights.loc[common_idx]

# Filter to active months (nonzero exposure)
mom_active = mom_weights.abs().sum(axis=1) > 0
rev_active = rev_weights.abs().sum(axis=1) > 0

# === Compute Average Monthly Return Statistics for MOM and REV ===
def compute_leg_stats(weights, returns):
    long_w = weights.where(weights > 0, 0)
    short_w = weights.where(weights < 0, 0)

    long_ret = (long_w * returns).sum(axis=1)
    short_ret = (short_w * returns).sum(axis=1)
    total_ret = (weights * returns).sum(axis=1)

    return {
        'long': long_ret.mean(),
        'short': short_ret.mean(),
        'total': total_ret.mean()
    }

mom_stats = compute_leg_stats(mom_weights.loc[mom_active], returns.loc[mom_active])
rev_stats = compute_leg_stats(rev_weights.loc[rev_active], returns.loc[rev_active])

# === Plot 1: Country Weights and Exposure Breakdown (MOM) ===
fig, ax = plt.subplots(figsize=(12, 6))
mom_weights.plot(ax=ax, linewidth=1, alpha=0.5)

# Add exposure breakdown lines
total = mom_weights.sum(axis=1)
longs = mom_weights.where(mom_weights > 0, 0).sum(axis=1)
shorts = mom_weights.where(mom_weights < 0, 0).sum(axis=1)

total.plot(ax=ax, color='black', linewidth=2, label='Total Weight')
longs.plot(ax=ax, color='green', linestyle='--', linewidth=1.5, label='Sum Positive (Long)')
shorts.plot(ax=ax, color='red', linestyle='--', linewidth=1.5, label='Sum Negative (Short)')

ax.axhline(0, linestyle='--', color='gray')
ax.set_title("MOM Strategy: Country Weights and Exposure Breakdown", fontsize=14)
ax.set_ylabel("Weight")
ax.set_xlabel("Date")
ax.legend(title="Legend")
ax.grid(True)
plt.tight_layout()
plt.show()

# === Plot 2: MOM Strategy — Avg Monthly Return (Bar Chart) ===
plt.figure(figsize=(6, 5))
plt.bar(["Long", "Short", "Total"], 
        [mom_stats['long'], mom_stats['short'], mom_stats['total']],
        color=["green", "red", "blue"])
plt.title("MOM Strategy: Avg Monthly Return", fontsize=14)
plt.ylabel("Return", fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# === Plot 3: REV Strategy — Avg Monthly Return (Bar Chart) ===
plt.figure(figsize=(6, 5))
plt.bar(["Long", "Short", "Total"], 
        [rev_stats['long'], rev_stats['short'], rev_stats['total']],
        color=["green", "red", "blue"])
plt.title("REV Strategy: Avg Monthly Return", fontsize=14)
plt.ylabel("Return", fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# === Plot 4: Scatterplot — MOM vs DIV with Regression Line ===
plt.figure(figsize=(6, 5))
sns.regplot(x=div, y=mom, ci=None, line_kws={'color': 'red'})
plt.title("MOM vs DIV", fontsize=14)
plt.xlabel("DIV Return", fontsize=12)
plt.ylabel("MOM Return", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()

# === Plot 5: Scatterplot — REV vs DIV with Regression Line ===
plt.figure(figsize=(6, 5))
sns.regplot(x=div, y=rev, ci=None, line_kws={'color': 'red'})
plt.title("REV vs DIV", fontsize=14)
plt.xlabel("DIV Return", fontsize=12)
plt.ylabel("REV Return", fontsize=12)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()


# %% [markdown]
# # Question 6: Currency Carry Strategy (CARRY)

# %% [markdown]
# ### 6.a) Construction of the return of the Carry Strategy portfolio

# %% [markdown]
# Calculation of the interest rate differentials ("carry") for the EUR, JPY, GBP, CHF and AUD currencies relative to the US dollar.

# %%
carry_df = ibexr.copy()

carry_df = carry_df.drop(columns="USD").subtract(ibexr["USD"], axis=0)

print('Interest rates differentials: \n')

print(carry_df.head())

# %% [markdown]
# Computation of the monthly portfolio weights by ranking currencies based on their interest rate differentials and scaling them so that the sum of long positions equals +1 and the sum of short positions equals −1.

# %%
N = carry_df.shape[1]
ranks = carry_df.rank(axis=1, method='first') # Highest interest rate differential --> Rank: 5 
center = (N + 1) / 2                          # Lowest interest rate differential --> Rank: 1
raw_scores = ranks - center

def compute_weights(row):
    long = row.clip(lower=0)
    short = row.clip(upper=0)
    Z_long = 1 / long.sum() if long.sum() != 0 else 0
    Z_short = -1 / short.sum() if short.sum() != 0 else 0
    return long * Z_long + short * Z_short

weights = raw_scores.apply(compute_weights, axis=1)

print('Monthly weights: \n')

print(weights.head())

# %% [markdown]
# Computation of the currency Carry Strategy's monthly returns

# %%
X = excess_return_currency_in_USD.copy()

# DEU and FRA have the same currency (EUR), so the same excess return currency. Thus we drop DEU, leave FRA and rename it EU.
X = X.drop(columns='DEU_currency_excess_return', errors='ignore')

# We Rename all country-based column to  match with the labels of our weights, which are also the currency ISO codes
rename_map = {
    'JPN_currency_excess_return': 'JPY',
    'AUS_currency_excess_return': 'AUD',
    'FRA_currency_excess_return': 'EUR',
    'CHE_currency_excess_return': 'CHF',
    'GBR_currency_excess_return': 'GBP'
}

X = X.rename(columns=rename_map)

weights.index = weights.index + pd.offsets.MonthEnd(1)

X = X[weights.columns]
W = weights.loc[X.index]  

# Final formula to compute our monthly returns
carry_ret = (W * X).sum(axis=1)

print('Carry Strategy monthly returns: \n')

print(carry_ret.head())


# %% [markdown]
# ### 6.b) Carry Strategy Performance

# %% [markdown]
#  Return calculations of the long and short legs of the Carry Strategy portfolio

# %%
long_leg = (W.clip(lower=0) * X).sum(axis=1)
short_leg = (W.clip(upper=0) * X).sum(axis=1)

print('Long leg monthly returns: \n')
print(long_leg.head())

print('\nShort leg monthly returns: \n')
print(short_leg.head())

# %% [markdown]
# Performance and risk analysis of the Carry Strategy, its long leg, and short leg and their statistical significance.

# %%
def stats_report(name, series):
    mean_monthly = series.mean()
    std_monthly = series.std()
    sharpe_monthly = mean_monthly / std_monthly if std_monthly != 0 else 0

    # Annualized results for more clarity
    mean_annual = mean_monthly * 12
    std_annual = std_monthly * np.sqrt(12)
    sharpe_annual = sharpe_monthly * np.sqrt(12)

    # t-test for significance
    n = len(series)
    t_stat = mean_monthly / (std_monthly / np.sqrt(n))
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))

    print(f"=== {name} ===")
    print(f"Annualized Mean Return: {mean_annual:.4%}")
    print(f"Annualized Std Dev: {std_annual:.4%}")
    print(f"Annualized Sharpe Ratio: {sharpe_annual:.2f}")
    print(f"t-statistic: {t_stat:.2f}, p-value: {p_val:.4f}")
    print(f"Statistically significant at 5%: {'Yes' if p_val < 0.05 else 'No'}\n")

stats_report("Carry Strategy", carry_ret)
stats_report("Long Leg", long_leg)
stats_report("Short Leg", short_leg)

# %% [markdown]
# ### Question 6.c) Regression analysis of the Carry strategy return on the DIV return

# %%
# Align carry and risk parity returns
carry_trimmed = carry_ret[carry_ret.index >= '2007-05-31']

# Ensure dates match
common_dates = carry_trimmed.index.intersection(rp_hedged.index)
Y = carry_trimmed.loc[common_dates]
X = rp_hedged.loc[common_dates].to_frame(name='DIV')  # Convert to DataFrame with column name 'RP'

# Add constant and run regression
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()

print(model.summary())



# %% [markdown]
# Plot of the regression of the Carry Strategy on DIV returns

# %%
plt.scatter(X["DIV"], Y, alpha=0.6, label="Data points")

x_vals = np.linspace(X["DIV"].min(), X["DIV"].max(), 100)
y_vals = model.params['const'] + model.params['DIV'] * x_vals

plt.plot(x_vals, y_vals, color='red', label='Fitted regression line')

plt.xlabel("DIV Return")
plt.ylabel("Carry Strategy Return")
plt.title("Carry Strategy vs DIV")
plt.legend()
plt.show()

# %% [markdown]
# # Question 7: Currency dollar Strategy (DOLLAR)

# %% [markdown]
# ### 7.a) Return construction of Currency Dollar Strategy (DOLLAR)

# %%
X = excess_return_currency_in_USD.copy()

# DEU and FRA have the same currency (EUR), so the same excess return currency. Thus we drop DEU, leave FRA and rename it EU.
X = X.drop(columns='DEU_currency_excess_return', errors='ignore')

# We Rename all country-based column to  match with the labels of our weights, which are also the currency ISO codes
rename_map = {
    'JPN_currency_excess_return': 'JPY',
    'AUS_currency_excess_return': 'AUD',
    'FRA_currency_excess_return': 'EUR',
    'CHE_currency_excess_return': 'CHF',
    'GBR_currency_excess_return': 'GBP'
}

X = X.rename(columns=rename_map)

#Monthly return of the Dollar Strategy
dollar_returns = - X.mean(axis=1).dropna()

print('Monthly return of the Dollar Strategy: \n')

print(dollar_returns.head())

# %% [markdown]
# ### Question 7.b) Performance and risk analysis of the Dollar Strategy and its statistical significance.

# %%
def stats_report(name, series):
    mean_monthly = series.mean()
    std_monthly = series.std()
    sharpe_monthly = mean_monthly / std_monthly if std_monthly != 0 else 0

    # Annualized results for more clarity
    mean_annual = mean_monthly * 12
    std_annual = std_monthly * np.sqrt(12)
    sharpe_annual = sharpe_monthly * np.sqrt(12)

    # t-test for significance
    n = len(series)
    t_stat = mean_monthly / (std_monthly / np.sqrt(n))
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=n - 1))

    print(f"=== {name} ===")
    print(f"Annualized Mean Return: {mean_annual:.4%}")
    print(f"Annualized Std Dev: {std_annual:.4%}")
    print(f"Annualized Sharpe Ratio: {sharpe_annual:.2f}")
    print(f"t-statistic: {t_stat:.2f}, p-value: {p_val:.4f}")
    print(f"Statistically significant at 5%: {'Yes' if p_val < 0.05 else 'No'}\n")

stats_report("Dollar Strategy", dollar_returns)

# %% [markdown]
# ### Question 7.c) Regression analysis of the Dollar Strategy return on the DIV returns

# %%
dollar_trimmed = dollar_returns[dollar_returns.index >= '2007-05-31']

# Ensure dates match
common_dates = dollar_trimmed.index.intersection(rp_hedged.index)
Y = dollar_trimmed.loc[common_dates]
X = rp_hedged.loc[common_dates].to_frame(name='DIV')  # Convert to DataFrame with column name 'RP'

# Add constant and run regression
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()

print(model.summary())

# %% [markdown]
# Plot of the regression of the Dollar Strategy on DIV returns

# %%
plt.scatter(X["DIV"], Y, alpha=0.6, label="Data points")

x_vals = np.linspace(X["DIV"].min(), X["DIV"].max(), 100)
y_vals = model.params['const'] + model.params['DIV'] * x_vals

plt.plot(x_vals, y_vals, color='red', label='Fitted regression line')

plt.xlabel("DIV Return")
plt.ylabel("Dollar Strategy Return")
plt.title("Dollar strategy vs DIV")
plt.legend()
plt.show()

# %% [markdown]
# Plot of the cumulative retuns of all the strategies 

# %%
# === Step 1: Ensure all strategy returns are 1D Series ===
mom_series    = pd.Series(mom, name="MOM")
rev_series    = pd.Series(rev, name="REV")
carry_series  = pd.Series(carry_ret, name="CARRY")
dollar_series = pd.Series(dollar_returns, name="DOLLAR")

# Handle DIV safely (may be DataFrame with one column)
if isinstance(div, pd.DataFrame):
    div_series = div.squeeze()
else:
    div_series = div.copy()
div_series.name = "DIV"

# === Step 2: Combine all into a single DataFrame and drop missing ===
all_returns_df = pd.concat([
    mom_series,
    rev_series,
    div_series,
    carry_series,
    dollar_series
], axis=1).dropna()

# === Step 3: Compute cumulative returns ===
cum_returns = (1 + all_returns_df).cumprod() - 1


plt.figure(figsize=(12, 6))
for col in cum_returns.columns:
    plt.plot(cum_returns.index, cum_returns[col], label=col)

plt.title("Cumulative Returns of Multi-Strategy Portfolio")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Optimal fund portfolio return (STRAT)

# %% [markdown]
# ### Question 8.1) 
# We have the fund return expressed as:
# 
# $$
# R_{\text{FUND}} = R_{\text{T-Bill}} + a(R_{\text{DIV}} - R_{\text{T-Bill}})
# $$
# 
# Since T-Bill rates are known one period in advance and have no uncertainty, the **variance of the fund** comes only from the excess return component:
# 
# $$
# \text{Var}(R_{\text{FUND}}) = a^2 \cdot \text{Var}(R_{\text{DIV}})
# $$
# 
# We want the **annualized volatility** of the fund to be 15% :
# 
# $$
# \text{Annualized Volatility} = a \cdot \sqrt{12 \cdot \text{Var}(R_{\text{DIV}})} = 0.15
# $$
# 
# which gives us :
# 
# $$
# a = \frac{0.15}{\sqrt{12 \cdot \text{Var}(R_{\text{DIV}})}}
# $$
# 
# To estimate $\text{Var}(R_{\text{DIV}})$, we use a **rolling window of 60 months**. For each time $t$, we compute the rolling variance and use the formula above to obtain the corresponding value of $a_t$ that targets a 15% annual volatility.
# 

# %%
rolling_volatilities_DIV = pd.Series(X['DIV'].rolling(window=60, min_periods=60).std().dropna())
a = 0.15 / (np.sqrt(12) * rolling_volatilities_DIV)
ax = a.plot()
plt.ylabel('Parameter a')
plt.xlabel('Date')
plt.title('Rolling Parameter a Over Time')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Question 8.2)

# %%
# Load U.S. Interest-Bearing rate data and process it (from 3 months T-Bill to monthly)
us_ib_rate = pd.read_csv("./data/USA_IB.csv")
us_ib_rate = us_ib_rate.rename(columns={'observation_date': 'date', 'IR3TIB01USM156N': 'us_ib_rate'})
us_ib_rate['date'] = pd.to_datetime(us_ib_rate['date']).dt.to_period('M')
us_ib_rate = us_ib_rate.sort_values('date').set_index('date')
us_ib_rate['us_ib_rate'] = (1 + us_ib_rate['us_ib_rate']/100)**(1/12) - 1 
us_ib_rate

# %%
# Compute mean, volatility, and Sharpe Ratio with risk-parity strategy
STRAT = pd.DataFrame({'MOM':mom_returns, 'REV':rev_returns, 'CARRY':carry_ret, 'DOLLAR':dollar_returns}).dropna()
STRAT_ret, STRAT_w = risk_parity_strategy(STRAT, window=60)
STRAT_w = STRAT_w.dropna()
STRAT_ret = STRAT_ret[STRAT_ret != 0].dropna()
STRAT_mean, STRAT_vol, STRAT_sr = portfolio_performance_SR(STRAT_ret, us_ib_rate['us_ib_rate'])

# %%
# Visualization
print(f"mean:{STRAT_mean}, Volatility:{STRAT_vol}, Sharpe Ratio:{STRAT_sr}")
STRAT_cumret = (1+STRAT_ret).cumprod()
STRAT_cumret.plot()

# %%
# Plotting the strategy weights over time
fig, ax = plt.subplots(figsize=(10, 6))
STRAT_w.plot(ax = ax)
ax.set_title("Stategy Weights Over Time")
ax.set_ylabel("Weights")
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Question 8.3)
# 
# We need to determine the weights of $(R_{DIV} - R_{T-Bill})$ and $R_{STRAT}$ for a mean variance investor

# %%
# Load T-Bill data and process it
tbill = pd.read_csv('./data/tbill.csv', sep=';').rename(columns={'mcaldt': 'date', 'tmytm': 'rate'})
tbill['rate'] = (1 + tbill['rate']/100)**(1/12)-1
tbill['date'] = pd.to_datetime(tbill['date'])
tbill = tbill.set_index('date')
tbill

# %%
# Create R_DIV, R_Tbill and R_STRAT
rdiv_rtbill_rstrat = pd.DataFrame({'DIV-Tbill':X['DIV']-tbill['rate'],'STRAT':STRAT_ret}).dropna()

# %%
# Function to compute tangency portfolio returns using MVO
def tangency_returns_mvo(returns: pd.DataFrame,rf : pd.Series,window:int=60)->pd.Series:
    # Align indexes of returns and risk-free rate
    common_index = returns.index.intersection(rf.index)
    returns = returns.loc[common_index]
    rf =rf.loc[common_index]
    # number of periods in the dataset
    n_periods = len(returns)
    # asset names
    a_names = returns.columns
    # stores portfolio weights
    pf_weights = []
    for t in range(window, n_periods):
        window_start = t-window
        window_end = t
        # Current window of returns
        window_position = returns.iloc[window_start:window_end]
        # rf of the previous period in the window
        rf_t =rf.iloc[t-1] 
        # Compute mean and covariance matrix of the window
        window_position_mean = window_position.mean()
        window_position_cov = window_position.cov()
        # Calculate excess returns over the risk-free rate
        window_excess_return = window_position_mean-rf_t
        # Formating
        period_w = pd.Series(np.zeros(len(a_names)), index=a_names) 
        cov_matrix = window_position_cov.to_numpy()
        excess_returns = window_excess_return.to_numpy()
        # Inverse covariance matrix
        inv_cov=np.linalg.inv(cov_matrix)
        # Calculate raw weights using the inverse covariance matrix and excess returns
        raw_weights = inv_cov@excess_returns 
        period_w = pd.Series(raw_weights, index=a_names)
        pf_weights.append(period_w)
    weights = pd.concat(pf_weights, axis=1).T
    weights.index = returns.index[window : n_periods]
    relevant_asset_returns = returns.iloc[window : n_periods]
    portfolio_returns = (weights * relevant_asset_returns).sum(axis=1)
    return portfolio_returns, weights

# %%
MVO_RET_FUND, MVO_FUND_weights= tangency_returns_mvo(rdiv_rtbill_rstrat, tbill['rate'], 60)
weights_lst = []
indexes = []
# Loop over each rolling window
for t in range(60,len(rdiv_rtbill_rstrat)): 
    rolling_window = rdiv_rtbill_rstrat.iloc[t-60:t-1]
    mu = rolling_window.mean().values
    sigma = rolling_window.cov().values
    # Formula: w = 0.15 * inv(sigma) * mu / sqrt(12 * mu.T * inv(sigma) * mu)
    w = 0.15*np.linalg.inv(sigma)@mu/np.sqrt(12*mu@np.linalg.inv(sigma)@mu)
    weights_lst.append(w)
    indexes.append(rdiv_rtbill_rstrat.index[t])
FUND_w = pd.DataFrame(weights_lst, index = indexes, columns = ['b','c'])
FUND_ret = (tbill['rate'] + FUND_w['b']*rdiv_rtbill_rstrat['DIV-Tbill'] + FUND_w['c']*STRAT_ret).dropna()
FUND_cumret = (1+FUND_ret).cumprod()

# %%
all_strat_w = pd.DataFrame({'DOLLAR' : FUND_w['c']*STRAT_w['DOLLAR'],'CARRY' : FUND_w['c']*STRAT_w['CARRY'],'MOM' : FUND_w['c']*STRAT_w['MOM'],
                                       'REV' : FUND_w['c']*STRAT_w['REV'],'DIV' : FUND_w['b'],'T-bill' : 1-FUND_w['b']  }).dropna()
all_strat_w

# %%
# Plotting the weights of all strategies with improved labels
ax = all_strat_w.plot(figsize=(12, 6))
ax.set_title("Fund Portfolio Weights Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Portfolio Weight")
plt.legend(title="Strategy")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### Question 8.4)

# %%
FUND_alt_ret = (tbill['rate']+a*(X['DIV']-tbill['rate'])).loc[FUND_ret.index].dropna()
FUND_alt_cumret = (1+FUND_alt_ret).cumprod() 
plt.figure(figsize=(10, 6))
plt.plot(FUND_alt_cumret.loc[FUND_cumret.index], label='Fund (DIV Only, Target Volatility)')
plt.plot(FUND_cumret,label='Fund (DIV + STRAT, Target Volatility)')
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.title("Cumulative Returns: Fund Strategies Comparison")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Calculate performance metrics
FUND_mean, vol_FUND, SR_FUND = portfolio_performance_SR(FUND_ret, us_ib_rate['us_ib_rate'])
FUND_mean_alt, vol_FUND_alt, SR_FUND_alt = portfolio_performance_SR(FUND_alt_ret, us_ib_rate['us_ib_rate'])
print("Fund Performance Comparison")
print("=" * 35)
print(f"{'':<25} {'Mean':>8} {'Volatility':>12} {'Sharpe Ratio':>15}")
print(f"{'With STRAT':<25} {FUND_mean:.4f}   {vol_FUND:.4f}      {SR_FUND:.2f}")
print(f"{'Without STRAT':<25} {FUND_mean_alt:.4f}   {vol_FUND_alt:.4f}      {SR_FUND_alt:.2f}")

# %% [markdown]
# ## 9. Performance and risk analysis for the Fund strategy

# %%
FUND_ret.index = FUND_ret.index.to_period('M')
FUND_alt_ret.index = FUND_alt_ret.index.to_period('M')

# %%
fama_french_factors = pd.read_csv("./data/ff_factors.csv")
fama_french_factors['date'] = pd.to_datetime(fama_french_factors['date'], format='%Y%m').dt.to_period('M')
fama_french_factors = fama_french_factors.set_index('date', inplace  = False)
fama_french_factors = fama_french_factors/100
fama_french_factors = fama_french_factors.loc[FUND_ret.index]
fama_french_factors

# %%
# Run OLS regression of FUND returns on Fama-French factors
y = FUND_ret
X = fama_french_factors
X = sm.add_constant(X)
model_FUND_on_FF = sm.OLS(y,X).fit()
print(model_FUND_on_FF.summary())


