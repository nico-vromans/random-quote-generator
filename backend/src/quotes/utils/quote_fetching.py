import logging
import random

from ..api.clients import BaseQuoteAPIClient
from ..api.models import Quote as QuoteData
from ..api.registry import API_CLIENTS
from ..enums import QuoteSource
from ..models import Quote
from ..utils.db_operations import get_or_create_quote

DATABASE = 'database'

logger = logging.getLogger('quotes')


def get_random_quote_source(excluded_sources: tuple = ()) -> QuoteSource:
    """
    Randomly choose a quote source (API client or database).
    """
    available_sources: list[QuoteSource] = [source for source in QuoteSource if source not in excluded_sources]

    if not available_sources:
        raise ValueError('No available quote sources after exclusion.')

    return random.choice(available_sources)


def fetch_random_quote_from_database(category: str = None) -> Quote | None:
    """
    Fetches a random quote from the database.
    """
    queryset = Quote.objects.all()
    if category:
        queryset = queryset.filter(category__name__icontains=category)
    return queryset.order_by('?').first()


def fetch_random_quote_from_api_client(quote_source: QuoteSource) -> Quote | None:
    api_client: BaseQuoteAPIClient | None = API_CLIENTS.get(quote_source.name)

    if api_client is None:
        return None
    else:
        try:
            quote: QuoteData | None = api_client.fetch_random_quote()

            return get_or_create_quote(quote=quote)
        except Exception as e:
            logger.exception(msg=e)

            return None


def fetch_random_quote() -> Quote | None:
    """Fetches a random quote from a random source."""
    try:
        quote_source: QuoteSource = get_random_quote_source()
        # quote_source: QuoteSource = QuoteSource.DATABASE
    except ValueError as e:
        logger.exception(msg=e)
        return None

    if quote_source == QuoteSource.DATABASE:
        quote: Quote | None = fetch_random_quote_from_database()

        if quote:
            return quote

        try:
            quote_source = get_random_quote_source(excluded_sources=(QuoteSource.DATABASE,))
        except ValueError as e:
            logger.exception(msg=e)
            return None

    quote: Quote | None = fetch_random_quote_from_api_client(quote_source=quote_source)

    return quote if quote else fetch_random_quote_from_database()
