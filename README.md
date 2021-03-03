# Portfolio Manager

This project can be used to get an overview of the portfolio based on the buy/sell transactions. Currently only DeGiro transaction overview is supported.

The project uses `yfinance` to get the latest price of the securities. 

## Installing and running
1. Install a  `python3.7` virtual environment. For instance by running `python3.7 -m venv venv/pm2`
2. Install the required packets `pip install -r requirements.txt` 
3. Run the script using `python src/position_overview.py -f example_transactions.csv`
4. The output should look like below:
```
                  Product          ISIN  Volume  Invested       Price        Value  Percent Change
Total                 NaN           NaN     NaN   7159.72         NaN  8295.324963       15.861025
2      ISHARES MSCI WOR A  IE00B4L5Y983   119.0   6500.16   62.535000  7441.664982       14.484335
1            ISHARES EMIM  IE00BKM4GZ66    20.0    526.06   31.462999   629.259987       19.617532
0      ISHARES E INF-LINK  IE00B0M62X26     1.0    219.91  224.399994   224.399994        2.041742
3                TAKEAWAY  NL0012015705     0.0    -86.41         NaN     0.000000     -100.000000

```