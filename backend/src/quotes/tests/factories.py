from django.conf import settings
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from contrib.constants import POSITIVE_BIT_INTEGER_MIN, POSITIVE_BIT_INTEGER_MAX
from quotes.models import Quote, Author, Category, QuoteOrigin

locale = settings.DEFAULT_TEST_LOCALE
fake = Faker(locale=locale)


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.Faker(provider='name', locale=locale)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker(provider='word', locale=locale)


class QuoteOriginFactory(DjangoModelFactory):
    class Meta:
        model = QuoteOrigin

    url = factory.Faker(provider='url', locale=locale)
    api_client_key = factory.Faker(provider='slug', locale=locale)


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote

    author = factory.SubFactory(factory=AuthorFactory)
    category = factory.SubFactory(factory=CategoryFactory)
    quote_text = factory.Faker(provider='paragraph', locale=locale)
    quote_hash = factory.Faker(provider='sha256', locale=locale)
    image_url = factory.Faker(provider='image_url', locale=locale)
    image_alt_text = factory.Faker(provider='sentence', locale=locale)
    origin = factory.SubFactory(QuoteOriginFactory)
    likes = factory.Faker(provider='random_int', min=POSITIVE_BIT_INTEGER_MIN, max=POSITIVE_BIT_INTEGER_MAX, locale=locale)
    dislikes = factory.Faker(provider='random_int', min=POSITIVE_BIT_INTEGER_MIN, max=POSITIVE_BIT_INTEGER_MAX, locale=locale)
