import logging
import random

from django.db import IntegrityError

from ..api.clients import BaseQuoteAPIClient
from ..api.models import Quote as QuoteData
from ..api.registry import API_CLIENTS
from ..enums import QuoteSource
from ..models import Quote
from ..utils.db_operations import get_or_create_quote

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


def fetch_random_quote_from_api_client(quote_source: QuoteSource = None, max_retries: int = 10) -> Quote | None:
    if quote_source is None:
        quote_source: QuoteSource = get_random_quote_source(excluded_sources=(QuoteSource.DATABASE,))

    api_client: BaseQuoteAPIClient | None = API_CLIENTS.get(quote_source.name)

    if api_client is None:
        return None

    attempts: int = 0
    while attempts < max_retries:
        try:
            # Get new random quote source
            quote_source: QuoteSource = get_random_quote_source(excluded_sources=(QuoteSource.DATABASE,))
            api_client: BaseQuoteAPIClient | None = API_CLIENTS.get(quote_source.name)

            if api_client is None:
                return None

            quote_data: QuoteData | None = api_client.fetch_random_quote()

            if quote_data is None:
                attempts += 1
                continue

            return get_or_create_quote(quote_data=quote_data)
        except IntegrityError:
            attempts += 1
        except Exception as e:
            attempts += 1
            logger.exception(msg=e)
        finally:
            if attempts >= max_retries:
                logger.exception(msg='Max retries reached. Unable to fetch random quote from API.')
                return None


def fetch_random_quote() -> Quote | None:
    """Fetches a random quote from a random source."""
    try:
        quote_source: QuoteSource = get_random_quote_source()
    except ValueError as e:
        logger.exception(msg=e)
        return None

    if quote_source == QuoteSource.DATABASE:
        quote: Quote | None = fetch_random_quote_from_database()

        if quote:
            return quote

    quote: Quote | None = fetch_random_quote_from_api_client()

    return quote if quote else fetch_random_quote_from_database()
