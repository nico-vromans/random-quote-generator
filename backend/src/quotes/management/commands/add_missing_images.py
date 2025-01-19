import logging
import time

import humanize
from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from pydantic import HttpUrl
from tqdm import tqdm

from contrib.api.clients import UnsplashImageAPIClient
from quotes.api.clients import BaseQuoteAPIClient
from quotes.api.registry import API_CLIENTS
from quotes.models import Quote

logger = logging.getLogger('quotes')


class Command(BaseCommand):
    help = 'Add images for quotes that have no image.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number_of_quotes',
            type=int,
            help='Number of quotes to update (default: %(default)s)',
            default=50,
        )

    def handle(self, *args, **options) -> None:
        start_time = time.time()
        number_of_quotes: int = options['number_of_quotes']

        self.stdout.write(self.style.SUCCESS(f'Searching for missing images for {number_of_quotes} quotes.'))

        success_count: int
        fail_count: int
        success_count, fail_count = 0, 0
        quotes_without_images: QuerySet = Quote.objects.filter(image_url__isnull=True).order_by('created')[
                                          :number_of_quotes]
        quotes_without_images_count: int = quotes_without_images.count()

        if quotes_without_images_count == 0:
            end_time = time.time()
            time_elapsed = humanize.precisedelta(end_time - start_time)

            self.stdout.write(
                self.style.SUCCESS(f'No quotes found that have missing images. Great! (took {time_elapsed})'))
            return None
        else:
            self.stdout.write(self.style.NOTICE(f'Found {quotes_without_images_count} quotes with missing images.'))

        with tqdm(total=quotes_without_images_count, desc="Processing missing images") as progress_bar:
            image_api_client = UnsplashImageAPIClient()

            for quote in quotes_without_images:
                try:
                    api_client: BaseQuoteAPIClient = API_CLIENTS.get(quote.origin.api_client_key)

                    if hasattr(api_client, 'image_search_query'):
                        image_search_query: str = getattr(api_client, 'image_search_query')
                    else:
                        image_search_query: str = quote.category.name

                    image_url: HttpUrl | None
                    image_alt_text: str | None
                    image_url, image_alt_text = image_api_client.get_random_image_with_parameters(
                        image_search_query=image_search_query)

                    if image_url is None:
                        fail_count += 1
                        continue

                    quote.image_url = image_url
                    quote.image_alt_text = image_alt_text
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
                f'Added images to {success_count} quotes ({fail_count} failed) - took {time_elapsed}.'))
