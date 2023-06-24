#!/bin/python3
"""
"""


# Standard Library imports.
from datetime import datetime, timedelta
from time import sleep


# In-House module imports.
# TODO: Replace with a built-in system.
from Lab93_DatabaseSystem import AdministratorDatabase


# Local sub-modules.
from .graphing.CandlestickGraphs import drawCandlestick
from .data import PriceData
from .data.historic import Queries
from .account import AccountDetails
from .trading import TradeBroker


# Establish connection with the credential database.
# NOTE: This is where we get our API credentials from.
AdminDB = AdministratorDatabase()


# Set datetime constants.
# NOTE: This is used for establishing a filepath to store generated assets.
today = datetime.today()
yesterday = today - timedelta(days=1)


# Establish connection to the broker API.
# This sets the account client for collecting data on our own holdings.
AlpacaAPI = AccountDetails(
    ( AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_key" ),
      AdminDB.Retrieve( user = "admin",
                        platform = "alpaca_secret" ) )
)


# Draw forth, the trading aspect of the brokerage account.
TradingBroker = TradeBroker(AlpacaAPI.client)


class GraphingReports:
    """
    This is the first Top-Level implementation of the graphing submodule; where we can access the underlying
    functionality in the form of a command-line API.
    """
    def __init__(self, start=yesterday, end=today, symbols: list = [ "BTC/USD" ]
        output = "/server/front-end/assets/data-science/reports" ):

        # Collect High, Low, Open, Close, and Times for the given symbol.
        # TODO: Allow for custom timeframes.
        # TODO: Retrieve credentials from environment.
        data = Queries( start = start, end = end, symbols = symbols,
                        timeframe = "hour",
                        credentials = ( AdminDB.Retrieve( user     = "admin",
                                                          platform = "alpaca_key" ),
                                        AdminDB.Retrieve( user     = "admin",
                                                          platform = "alpaca_secret" ) ) )\
               .HLOC()\
               .data

        # Convert start date into string separated by forward slashes.
        datestring = datetime.strftime(start, "%Y/%m/%d")

        # Organize data array into packet hashmap for passing to Candlestick class.
        drawCandlestick( {

            "time":   [ line.timestamp for symbol in data for line in data[symbol] ],
            "high":   [ line.high for symbol in data for line in data[symbol]      ],
            "low":    [ line.low for symbol in data for line in data[symbol]       ],
            "open":   [ line.open for symbol in data for line in data[symbol]      ],
            "close":  [ line.close for symbol in data for line in data[symbol]     ],
            "symbol": [ line.symbol for symbol in data for line in data[symbol] ][0]

        }, f"{output}/{datestring}")
