from pathlib import Path
import pandas as pd

def _loader(folder="./", loockback=100)-> pd.DataFrame:
    folder = Path(folder)
    stocks    = []

    for file in folder.glob("*.csv"):
        stock          =  file.stem
        df             =  pd.read_csv(file)
        df["Date"]     =  pd.to_datetime(df["Date"])            # Convert date
        df             =  (df.sort_values("Date"))             # Set index
        df["Stock"]    =  stock
        stocks.append(df)

    master                =  (pd.concat(stocks, ignore_index=True))
    all_dates             =  master["Date"].unique()
    all_stocks            =  master["Stock"].unique()
    
    template              = (pd.MultiIndex.from_product(
                             [all_dates, all_stocks],
                             names=["Date", "Stock"])
                            .to_frame(index=False)
                             )
    
    master              = template.merge(
                            master,
                            on=["Date", "Stock"],
                            how="left"
                            )
    
    ohlcv_cols          =  ["Open", "High", "Low", "Close", "Change", "Volume"]
    master              =  master.sort_values(["Stock", "Date"])
    master[ohlcv_cols]  =  (master.groupby("Stock")[ohlcv_cols].ffill())
    master[ohlcv_cols]  =  (master[ohlcv_cols]
                                .apply(lambda col: pd.to_numeric(col, errors="coerce")
                                .fillna(0)
                                 ))

    master             =  (master.sort_values(["Stock", "Date"])
                              .reset_index(drop=True)
                              .groupby("Stock")
                              .tail(loockback)
                              )
  
    master['% Change']    = (master["Change"] * 100)
    master['Change']      = (master["Change"] * master["Close"])
    valid_cols            = ["Date", "Stock", "Open", "High", "Low", "Close", "Change", "% Change", "Volume"]
    
    return master[valid_cols]