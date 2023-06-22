from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests   import CryptoLatestQuoteRequest

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests   import StockLatestQuoteRequest

from Lab93_DatabaseSystem import AdministratorDatabase


class PriceData:
    def __init__(self, asset_type, credentials):


        self.asset_type = asset_type.lower()

        if self.asset_type   == "stocks":
            self.client = StockHistoricalDataClient( credentials[0],
                                                     credentials[1] )

        elif self.asset_type == "crypto":
            self.client = CryptoHistoricalDataClient( credentials[0],
                                                      credentials[1] )


    def CurrentPrice(self, symbol):


        if self.asset_type == "stocks":
            parameters = StockLatestQuoteRequest( symbol_or_symbols = symbol )
            quote = self.client\
                        .get_stock_latest_quote( parameters )

        elif self.asset_type == "crypto":
            parameters = CryptoLatestQuoteRequest( symbol_or_symbols = symbol )
            quote = self.client\
                        .get_crypto_latest_quote( parameters )

        return quote[symbol].ask_price

# Establish connection with the credential database.
# NOTE: This is where we get our API credentials from.
AdminDB = AdministratorDatabase()


# Set current price constants.
# NOTE: This one provides the current price of a valid cryptocurrency asset.
CryptoPrices = PriceData(
    asset_type = "crypto", credentials = \
    ( AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_key" ),
      AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_secret" ) )
)


# NOTE: This one provides the current price of a valid stock market asset.
StockPrices = PriceData(
    asset_type = "stocks", credentials = \
    ( AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_key" ),
      AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_secret" ) )
)


def Ticker(asset, symbol):
    """
    A simple generator for selecting either of the price daemons and setting a stream handler to
    recieve the data emanating from the generator.
    """

    # Select the stock daemon.
    if asset.lower() == "stocks": daemon = StockPrices

    # Select the crypto daemon.
    elif asset.lower() == "crypto": daemon = CryptoPrices

    # Execute the generator.
    while True:
        sleep(1)
        yield format(daemon.CurrentPrice(symbol), ".2f")

