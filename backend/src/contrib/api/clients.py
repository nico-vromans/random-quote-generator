import logging
from typing import Any

import requests
from django.conf import settings
from pydantic import HttpUrl
from requests import Response

logger = logging.getLogger('contrib')


class UnsplashImageAPIClient:
    BASE_API_URL = 'https://api.unsplash.com'

    def get_random_image_with_parameters(self, image_search_query: str) -> tuple[HttpUrl, Any | None] | None:
        try:
            params: dict[str, any] = {
                'client_id': settings.UNSPLASH_API_CLIENT_ID,
                'query': image_search_query,
                'orientation': 'landscape',
                'content_filter': 'high',
            }

            response: Response = requests.get(self.BASE_API_URL + '/photos/random', params=params)
            data: dict[str, any] = response.json()
            image_url: str | None = data.get('urls').get('regular')
            image_alt_text: str | None = data.get('alt_description')

            return HttpUrl(image_url), image_alt_text
        except Exception as e:
            logger.exception(msg=e)

            return None
