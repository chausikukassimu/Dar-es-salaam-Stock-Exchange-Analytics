TICKERS = ["AFRIPRISE", "CRDB", "DCB", "DSE", "EABL", "JATU", "JHL", "KA", "KCB", 
    "MBP", "MCB", "MKCB", "MUCOBA", "NICO", "NMB", "NMG", "PAL", "SWALA", "SWIS",
    "TBL", "TCC", "TCCL", "TOL", "TPCC", "TTP", "USL", "VODA", "YETU", 
    "VERTEX ETF", "ITRUST ETF"
    ]


TRADING_DAYS           = 252         # Annual trading days
RISK_FREE_RATE         = 0.08        # 8% — Tanzania T-Bill proxy
CONFIDENCE_LEVEL       = 0.95        # 95% VaR
MC_SIMULATIONS         = 10_000      # Monte Carlo paths
MC_HORIZON             = 252         # 1-year projection
LOOK_BACK              = 710
DATA_FOLDER           = './Datasets'
