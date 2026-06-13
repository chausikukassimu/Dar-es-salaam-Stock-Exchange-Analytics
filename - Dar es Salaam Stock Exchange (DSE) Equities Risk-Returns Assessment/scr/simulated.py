import pandas as pd
import numpy as np
np.random.seed(42)

def _simulation(stocks, periods=800):
    dates   = pd.bdate_range('2024-01-01', periods=852)
    records = []
    
    for stock in stocks:
        price = 100 + np.random.uniform(-20,20)
        for date in dates:
            ret      =  np.random.normal(0.0005,0.02)
            close    =  price * (1+ret)
            open_    =  price
            change   =  open_-close
            high     =  max(open_, close) * (1 + np.random.uniform(0,0.02))
            low      =  min(open_, close) * (1 - np.random.uniform(0,0.02))
            volume   =  np.random.randint(1000,20000)
            turnover = (close * volume)
            mkt_cap  =  np.random.randint(20, 1000)
            
    
            records.append([date, stock, open_, high, low, close, change, ret, volume, turnover, mkt_cap])

    columns =  ['Date','Stock','Open','High','Low','Close', 'Change', '% Change','Volume', 'Turnover', 'Markert Cap']
    df      =  pd.DataFrame(records, columns=columns)
    
    return df
