import time
import random
import logging

from tqdm import tqdm
import humanize

from django.core.management.base import BaseCommand

from quotes.enums import QuoteSource
from quotes.models import Quote
from quotes.utils.quote_fetching import get_random_quote_source, fetch_random_quote_from_api_client

logger = logging.getLogger('quotes')


class Command(BaseCommand):
    help = 'Pre-populate the database with quotes from various sources.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number_of_quotes',
            type=int,
            help='Number of quotes to fetch',
            default=50,
        )
        parser.add_argument(
            '--random_likes',
            type=bool,
            help='Set random likes and dislikes',
            default=True,
        )

    def handle(self, *args, **options) -> None:
        start_time = time.time()
        number_of_quotes: int = options['number_of_quotes']

        self.stdout.write(self.style.SUCCESS(f'Pre-populating database with {number_of_quotes} quotes.'))

        random_likes: bool = options['random_likes']
        success_count: int
        fail_count: int
        success_count, fail_count = 0, 0

        with tqdm(total=number_of_quotes, desc="Processing quotes") as progress_bar:
            for i in range(number_of_quotes):
                try:
                    quote_source: QuoteSource = get_random_quote_source(excluded_sources=(QuoteSource.DATABASE,))
                    quote: Quote | None = fetch_random_quote_from_api_client(quote_source=quote_source)

                    if quote is not None and random_likes:
                        # set random likes/dislikes
                        lower, upper = 0, 99_9999
                        quote.likes = random.randint(lower, upper)
                        quote.dislikes = random.randint(lower, upper)
                        quote.save()
                        success_count += 1
                except Exception as e:
                    logger.exception(msg=e)
                    fail_count += 1
                finally:
                    progress_bar.update(1)

        end_time = time.time()
        time_elapsed = humanize.precisedelta(end_time - start_time)

        self.stdout.write(
            self.style.SUCCESS(
                f'Pre-populated the database with {success_count} quotes ({fail_count} failed) - took {time_elapsed}.'))
