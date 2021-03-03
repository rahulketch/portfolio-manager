import pandas
import yfinance as yf
import argparse

def ticker_from_isin(isin):
    return {
        'IE00B4L5Y983': 'IWDA.AS',
        'IE00B0M62X26': 'IBCI.AS',
        'IE00B1FZSC47': 'TPSA.AS',
        'IE00BKM4GZ66': 'EMIM.AS',
        'NL0012015705': 'TKWY.AS'
    }[isin]


def read_degiro_transactions(filepath):
    df = pandas.read_csv(filepath)
    column_rename = {
        'Datum': 'Date',
        'ISIN': 'Ticker',
        'Aantal': 'Volume',
        'Koers': 'Price',
        'Totaal': 'Invested'
    }
    df = df[column_rename.keys()].rename(columns=column_rename)
    df['Invested'] = -1 * df['Invested'].fillna(0)
    df['Ticker'] = df['Ticker'].apply(ticker_from_isin)
    return df


def get_ticker_price(ticker):
    return yf.Ticker(ticker).history(period="1d")['Close'][0]


def get_positions(df):
    positions = df.groupby('Ticker').agg({'Volume': 'sum', 'Invested': 'sum'}).reset_index()
    positions['Price'] = positions['Ticker'].apply(get_ticker_price)
    positions['Value'] = positions['Volume'] * positions['Price']
    positions.loc["Total"] = positions[['Value', 'Invested']].sum()
    positions['Percent Change'] = (positions['Value'] - positions['Invested']) / positions['Invested'] * 100

    return positions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    args = parser.parse_args()
    transactions = read_degiro_transactions(args.file)
    positions = get_positions(transactions)
    print(positions)


if __name__ == "__main__":
    main()
