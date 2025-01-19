import pytest
from pydantic import HttpUrl

from contrib.constants import POSITIVE_BIT_INTEGER_MIN, POSITIVE_BIT_INTEGER_MAX
from contrib.tests.assertions import is_valid_sha256
from quotes.models import Quote, Author, Category, QuoteOrigin
from quotes.tests.factories import QuoteFactory


@pytest.mark.django_db
def test_quote_model():
    quote = QuoteFactory()

    assert isinstance(quote, Quote)
    assert isinstance(quote.quote_text, str)
    assert isinstance(quote.quote_hash, str)
    assert len(quote.quote_hash) == 64
    assert is_valid_sha256(quote.quote_hash) is True
    assert isinstance(quote.image_url, str)
    assert quote.image_url.startswith('http')
    assert isinstance(quote.image_alt_text, str)
    assert isinstance(quote.likes, int)
    assert quote.likes >= POSITIVE_BIT_INTEGER_MIN
    assert quote.likes <= POSITIVE_BIT_INTEGER_MAX
    assert isinstance(quote.dislikes, int)
    assert quote.dislikes >= POSITIVE_BIT_INTEGER_MIN
    assert quote.dislikes <= POSITIVE_BIT_INTEGER_MAX
    assert isinstance(quote.author, Author)
    assert isinstance(quote.author.name, str)
    assert isinstance(quote.category, Category)
    assert isinstance(quote.category.name, str)
    assert isinstance(quote.origin, QuoteOrigin)
    assert isinstance(quote.origin.url, str)
    assert quote.origin.url.startswith('http')
    assert isinstance(quote.origin.api_client_key, str)
