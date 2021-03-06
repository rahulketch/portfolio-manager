import pandas
import yfinance as yf
import argparse


def ticker_from_isin(isin):
    mapping = {
        'IE00B4L5Y983': 'IWDA.AS',
        'IE00B0M62X26': 'IBCI.AS',
        'IE00B1FZSC47': 'TPSA.AS',
        'IE00BKM4GZ66': 'EMIM.AS',
        'US21833P1030': 'CRBP',
        'US2210151005': 'CRVS',
        'US39874R1014': 'GO'
    }

    if isin in mapping:
        return mapping[isin]
    else:
        return None


class PortfolioOverview:
    def __init__(self, files):
        self.eur_usd_conversion = yf.Ticker('EURUSD=X').history(period="1d")['Close'][0]
        self.transactions = pandas.concat([self._read_degiro_transactions(file) for file in files])
        self.positions = self._get_positions()

    def _get_positions(self):
        def _get_current_value(row):
            if row.Volume == 0:
                return 0
            if pandas.isna(row.Price):
                raise RuntimeError(f"{row.ISIN} has no price")
            return row.Price * row.Volume

        def get_ticker_price(isin):
            ticker_name = ticker_from_isin(isin)
            if ticker_name is None:
                return None
            ticker = yf.Ticker(ticker_name)
            price = ticker.history(period="1d")['Close'][0]
            if ticker.info['currency'] == 'EUR':
                return price
            elif ticker.info['currency'] == 'USD':
                return price / self.eur_usd_conversion
            else:
                raise RuntimeError(f"Currency {ticker.info['currency']} not supported")

        positions = self.transactions.groupby(['Product', 'ISIN']).agg({'Volume': 'sum', 'Invested': 'sum'}).reset_index()
        positions['Price'] = positions['ISIN'].apply(get_ticker_price)
        positions['Value'] = positions.apply(_get_current_value, axis=1)
        positions.loc["Total"] = positions[['Value', 'Invested']].sum()
        positions['Percent Change'] = (positions['Value'] - positions['Invested']) / positions['Invested'] * 100
        return positions.sort_values('Value', ascending=False)

    @staticmethod
    def _read_degiro_transactions(filepath):
        df = pandas.read_csv(filepath)
        column_rename = {
            'Datum': 'Date',
            'Product': 'Product',
            'ISIN': 'ISIN',
            'Aantal': 'Volume',
            'Koers': 'Price',
            'Totaal': 'Invested',
        }
        df = df[column_rename.keys()].rename(columns=column_rename)
        df['Invested'] = -1 * df['Invested'].fillna(0)
        return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', nargs='+')
    args = parser.parse_args()
    portfolio_overview = PortfolioOverview(args.files)
    print(portfolio_overview.positions.to_string())


if __name__ == "__main__":
    main()
