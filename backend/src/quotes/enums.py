from enum import Enum

from quotes.api.registry import API_CLIENTS

QuoteSource = Enum('QuoteSource', {'DATABASE': 'database', **API_CLIENTS})
