import logging

from pydantic import HttpUrl

from contrib.api.clients import UnsplashImageAPIClient
from ..api.models import Quote as QuoteData
from ..models import Quote, Author, Category, QuoteOrigin

logger = logging.getLogger('quotes')


def get_or_create_quote(quote: QuoteData | None) -> Quote | None:
    """
    Saves a quote to the database if not already present.
    """
    if quote is None:
        return

    author: str = quote.author
    category: str = quote.category
    image_search_query: str | None = quote.image_search_query
    origin: HttpUrl = quote.origin
    quote_text: str = quote.quote_text
    api_client_key: str = quote.api_client_key

    try:
        author: Author
        author, _ = Author.objects.get_or_create(name=author)
        category: Category
        category, _ = Category.objects.get_or_create(name=category)
        quote_origin: QuoteOrigin
        quote_origin, _ = QuoteOrigin.objects.get_or_create(url=origin, api_client_key=api_client_key)
        image_url: HttpUrl | None
        image_alt_text: str | None
        image_url, image_alt_text = UnsplashImageAPIClient().get_random_image_with_parameters(
            image_search_query=image_search_query)
        quote: Quote
        quote, created = Quote.objects.get_or_create(
            author=author,
            category=category,
            image_url=image_url,
            image_alt_text=image_alt_text,
            origin=quote_origin,
            quote_text=quote_text,
            defaults={'author': author, 'category': category, 'origin': quote_origin},
        )

        return quote
    except Exception as e:
        logger.exception(msg=e)

        return None
