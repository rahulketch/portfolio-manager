# Portfolio Manager

Portfolio manager can be used to get an overview of a financial instruments portfolio. Currently only transaction overview from Degiro are supported


## Installing and running
1. Install a  `python3.7` virtual environment. For instance by running `python3.7 -m venv venv/pm2`
2. Install the required packets `pip install -r requirements.txt` 
3. Run the script using `python src/position_overview.py -f example_transactions.csv`
4. The output should look like below:
```
        Ticker  Volume  Invested       Price         Value  Percent Change
0      EMIM.AS   260.0   6368.99   31.455000   8178.299980       28.408115
1      IBCI.AS    14.0   3083.95  224.539993   3143.559906        1.932908
2      IWDA.AS   810.0  42213.66   62.380001  50527.800865       19.695380
3      TKWY.AS     0.0    -86.41   77.739998      0.000000     -100.000000
4      TPSA.AS    13.0   2600.88  199.199997   2589.599960       -0.433701
Total      NaN     NaN  54181.07         NaN  64439.260712       18.933164
```