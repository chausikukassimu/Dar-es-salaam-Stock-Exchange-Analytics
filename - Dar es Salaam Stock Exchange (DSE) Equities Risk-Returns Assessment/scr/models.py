import pandas as pd
import numpy as np

def _return_volatility(df, stock_col='Stock', date_col='Date', price_col="Close", annualize=True):
    df             =   df.copy()
    df             =   df.sort_values([stock_col, date_col])
    df             =   df[[date_col, stock_col, price_col]]
    df['1 D']      =   (df.groupby(stock_col)[price_col].pct_change())
    horizons = {
        '1W': 5,
        '1M': 21,
        '3M': 63,
        '6M': 126,
        '1Y': 252
        }
    
    for label, periods in horizons.items():
        df[f'{label} Return'] = (
            df.groupby(stock_col)[price_col]
              .pct_change(periods)
              ) * 100

    for label, window in horizons.items():
        vol = (df.groupby(stock_col)['1 D']
              .rolling(window)
              .std()
              .reset_index(level=0, drop=True)
              ) * 100

        if annualize:  vol *=  np.sqrt(252)
        df[f'{label} Vol']   =  vol

    return df

class modeli:
    def __init__(self, df, date_col="Date", stock_col="Stock", freqs = ['W']):
        self.df             =  df.copy()
        self.date_col       =  date_col
        self.stock_col      =  stock_col
        self.freqs          =  freqs
        self.df[date_col]   =  pd.to_datetime(self.df[date_col])
        self.df             =  df.sort_values([self.stock_col, self.date_col])

    def _compute(self, df, result, value_col, freq):
        data = (df.groupby([self.stock_col,pd.Grouper(key=self.date_col, freq=freq)])[value_col]
            .sum()
            .reset_index()
            )

        data[f"P{freq}"]  = (data.groupby(self.stock_col)[value_col].shift(1))
        _latest           = (data.groupby(self.stock_col).tail(1))

        result[f"{freq}TD"]         = _latest[value_col].values
        result[f"P{freq}"]          = _latest[f"P{freq}"].values
        result[f"{freq}o{freq}"]    = (result[f"{freq}TD"] - result[f"P{freq}"])
        result[f"{freq}o{freq} %"]  = (result[f"{freq}o{freq}"] / result[f"P{freq}"]) * 100

        return result

    def compute(self, value_col: np.number) -> pd.DataFrame:
        df            =  self.df.copy()
        latest_date   =  df[self.date_col].max()
        
        current = (
            df[df[self.date_col] == latest_date]
            [[self.stock_col, value_col]]
            .rename(columns={value_col: "Today"})
            )

        previous = (
            df[df[self.date_col] < latest_date]
            .sort_values(self.date_col)
            .groupby(self.stock_col)
            .tail(1)
            [[self.stock_col, value_col]]
            .rename(columns={value_col: "PD"})
            )

        result = current.merge( previous, on=self.stock_col, how="left" )
        
        result["DoD"]     = (result["Today"] - result["PD"])
        result["DoD %"]   = (result["DoD"] / result["PD"]) * 100

        for freq in self.freqs: results = self._compute(df, result, value_col, freq=freq)

        return results