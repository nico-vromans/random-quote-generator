import logging
import random

from ..api.models import Quote as QuoteData
from ..api.registry import API_CLIENTS
from ..enums import QuoteSource
from ..models import Quote
from ..utils.db_operations import get_or_create_quote

DATABASE = 'database'

logger = logging.getLogger('quotes')


def get_random_quote_source() -> QuoteSource:
    """
    Randomly choose a quote source (API client or database).
    """
    sources: list[QuoteSource] = list(QuoteSource)

    return random.choice(sources)


def fetch_random_quote_from_database() -> Quote | None:
    """
    Fetches a random quote from the database.
    """
    return Quote.objects.order_by('?').first()


def fetch_random_quote() -> Quote | None:
    """Fetches a random quote from a random source."""
    quote_source: QuoteSource = get_random_quote_source()

    if quote_source == QuoteSource.DATABASE:
        return fetch_random_quote_from_database()

    api_client = API_CLIENTS.get(quote_source.name)

    if api_client is None:
        return None
    else:
        try:
            quote: QuoteData | None = api_client.fetch_random_quote()

            return get_or_create_quote(quote=quote)
        except Exception as e:
            logger.exception(msg=e)

            return fetch_random_quote_from_database()
