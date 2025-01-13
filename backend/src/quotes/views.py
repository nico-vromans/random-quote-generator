from http import HTTPMethod

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import QuoteSerializer
from .utils.quote_fetching import fetch_random_quote


class QuoteViewSet(viewsets.ViewSet):
    """
    API endpoints for getting quotes.
    """
    serializer_class = QuoteSerializer

    @action(detail=False, methods=[HTTPMethod.GET])
    def get_random_quote(self, request: Request) -> Response:
        """
        Get a random quote.
        """
        quote = fetch_random_quote()
        serializer = QuoteSerializer(quote)

        return Response(serializer.data)
