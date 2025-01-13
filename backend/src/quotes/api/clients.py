import logging
from abc import ABC, abstractmethod
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests import Response

from quotes.api.models import Quote

logger = logging.getLogger('quotes')


class BaseQuoteAPIClient(ABC):
    """
    Abstract Base Class for handling quotes from an API.
    """

    @property
    @abstractmethod
    def base_url(self) -> str:
        raise NotImplementedError('Subclasses must implement ``base_url``!')

    @property
    @abstractmethod
    def random_quote_url(self) -> str:
        raise NotImplementedError('Subclasses must implement ``random_quote_url``!')

    @abstractmethod
    def fetch_random_quote(self) -> Quote | None:
        raise NotImplementedError('Subclasses must implement ``fetch_random_quote``!')


class APINinjaQuoteAPIClient(BaseQuoteAPIClient):
    @property
    def base_url(self) -> str:
        return 'https://api.api-ninjas.com/'

    @property
    def random_quote_url(self) -> str:
        return urljoin(base=self.base_url, url='v1/quotes')

    def fetch_random_quote(self) -> Quote | None:
        try:
            headers: dict[str, any] = {
                'X-Api-Key': settings.APININJAS_API_KEY,
            }
            response: Response = requests.get(url=self.random_quote_url, headers=headers)
            data: dict[str, any] = response.json()[0]
            author: str | None = data.get('author')
            category: str | None = data.get('category')
            quote_text: str | None = data.get('quote')
            quote_data: dict[str, any] = {
                'author': author, 'category': category, 'image_search_query': category, 'origin': self.base_url,
                'quote_text': quote_text
            }

            return Quote(**quote_data)
        except Exception as e:
            logger.exception(msg=e)

            return None


class ProgrammingQuoteAPIClient(BaseQuoteAPIClient):
    @property
    def base_url(self) -> str:
        return 'https://programming-quotesapi.vercel.app/api/'

    @property
    def random_quote_url(self) -> str:
        return urljoin(base=self.base_url, url='random')

    @property
    def category(self) -> str:
        return 'programming'

    @property
    def image_search_query(self) -> str:
        return 'code,programming,programmer'

    def fetch_random_quote(self) -> Quote | None:
        try:
            response: Response = requests.get(url=self.random_quote_url)
            data: dict[str, any] = response.json()
            author: str = data.get('author')
            quote_text: str = data.get('quote')
            quote_data: dict[str, any] = {
                'author': author, 'category': self.category, 'image_search_query': self.image_search_query,
                'origin': self.base_url, 'quote_text': quote_text
            }

            return Quote(**quote_data)
        except Exception as e:
            logger.exception(msg=e)

            return None


class ZenQuoteAPIClient(BaseQuoteAPIClient):
    @property
    def base_url(self) -> str:
        return 'https://zenquotes.io/api/'

    @property
    def random_quote_url(self) -> str:
        return urljoin(base=self.base_url, url='random')

    @property
    def category(self) -> str:
        return 'zen'

    @property
    def image_search_query(self) -> str:
        return 'zen,yoga,mindfulness'

    def fetch_random_quote(self) -> Quote | None:
        try:
            response: Response = requests.get(url=self.random_quote_url)
            data: list[dict[str, any]] = response.json()
            author: str = data[0].get('a')
            quote_text: str = data[0].get('q')
            quote_data: dict[str, any] = {
                'author': author, 'category': self.category, 'image_search_query': self.image_search_query,
                'origin': self.base_url, 'quote_text': quote_text
            }

            return Quote(**quote_data)
        except Exception as e:
            logger.exception(msg=e)

            return None
