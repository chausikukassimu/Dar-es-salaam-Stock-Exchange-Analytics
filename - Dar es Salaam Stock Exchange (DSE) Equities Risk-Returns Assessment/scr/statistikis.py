import statsmodels.api as sm
import pandas as pd
import numpy as np


TRADING_DAYS           = 252         # Annual trading days
RISK_FREE_RATE         = 0.08        # 8% — Tanzania T-Bill proxy
CONFIDENCE_LEVEL       = 0.95        # 95% VaR


def ann_return(returns, ann_factor=TRADING_DAYS):
    """Compound Annual Growth Rate"""
    cum = (1 + returns).prod()
    n_years = len(returns) / ann_factor
    return cum ** (1 / n_years) - 1

def ann_vol(r):     return r.std() * np.sqrt(252)

def sharpe(returns, rf=RISK_FREE_RATE, ann_factor=TRADING_DAYS):
    """Annualized Sharpe Ratio"""
    daily_rf = rf / ann_factor
    excess   = returns - daily_rf
    if excess.std() == 0:
        return np.nan
    return (excess.mean() / excess.std()) * np.sqrt(ann_factor)

def sortino(returns, rf=RISK_FREE_RATE, ann_factor=TRADING_DAYS):
    """Sortino Ratio — penalizes downside volatility only"""
    daily_rf  = rf / ann_factor
    excess    = returns - daily_rf
    downside  = returns[returns < 0].std() * np.sqrt(ann_factor)
    if downside == 0:
        return np.nan
    return (excess.mean() * ann_factor) / downside

def max_dd(r):
    """Maximum Drawdown — largest peak-to-trough decline"""
    cum   = (1 + r).cumprod()
    peak  = cum.cummax()
    dd    = (cum - peak) / peak
    mdd   = dd.min()
    trough_date = dd.idxmin()
    post  = cum[trough_date:]
    rec   = post[post >= peak[trough_date]]
    rec_days = (rec.index[0] - trough_date).days if not rec.empty else None
    return mdd, trough_date, dd, rec_days

def calmar(returns, ann_factor=TRADING_DAYS):
    """Calmar = CAGR / |Max Drawdown|"""
    mdd,_,_,_ = max_dd(returns)
    if mdd == 0:
        return np.nan
    return ann_return(returns, ann_factor) / abs(mdd)

def var_cvar(returns, confidence=CONFIDENCE_LEVEL):
    var = returns.quantile(1 - confidence)
    cvar = returns[returns <= var].mean()
    return var, cvar

def omega_ratio(returns, rf=RISK_FREE_RATE, ann_factor=TRADING_DAYS):
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan

    threshold = (1 + rf)**(1 / ann_factor) - 1
    gains     = np.maximum(returns - threshold, 0)
    losses    = np.maximum(threshold - returns, 0)
    total_losses = losses.sum()
    if total_losses == 0: return np.nan

    return gains.sum() / total_losses

def beta_alpha(returns, benchmark, rf=RISK_FREE_RATE, ann_factor=TRADING_DAYS):
    df = pd.concat([returns.rename("asset"), benchmark.rename("market")], axis=1).dropna()

    if len(df) < 30: return np.nan, np.nan, np.nan, None

    rf_daily = (1 + rf)**(1 / ann_factor) - 1
    asset_excess   = df["asset"] - rf_daily
    market_excess  = df["market"] - rf_daily
    X              = sm.add_constant(market_excess)
    model          = sm.OLS(asset_excess, X).fit()
    alpha_daily    = model.params.iloc[0]
    beta           = model.params.iloc[1]
    alpha_annual   = (1 + alpha_daily)**ann_factor - 1

    return beta, alpha_annual, model.rsquared
    
