from http import HTTPMethod

from distutils.util import strtobool
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from contrib.views import GenericGUIDViewSet
from .models import Quote
from .serializers import QuoteSerializer
from .utils.quote_fetching import fetch_random_quote


class QuoteViewSet(GenericGUIDViewSet, ListAPIView, RetrieveAPIView, viewsets.ViewSet):
    """
    API endpoints for getting quotes.
    """
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()

    @action(detail=False, methods=[HTTPMethod.GET])
    def get_random_quote(self, request: Request) -> Response:
        """
        Get a random quote.
        """
        quote: Quote = fetch_random_quote()
        serializer = QuoteSerializer(quote)

        return Response(serializer.data)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                name='direction',
                description='Add or remove count.',
                required=True,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                enum=['increase', 'decrease'],
            ),
            OpenApiParameter(
                name='reverse_opposite',
                description='Reverse vote (remove the opposite rating).',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
            )
        ],
    )
    @action(detail=True, methods=[HTTPMethod.PATCH])
    def like(self, request: Request, guid: str) -> Response:
        """
        Like a quote.
        """
        direction = request.query_params.get('direction', 'increase')
        quote: Quote = Quote.objects.get(guid=guid)

        if direction == 'increase':
            quote.likes += 1

            reverse_opposite: bool = bool(strtobool(request.query_params.get('reverse_opposite', '0')))

            if reverse_opposite and quote.dislikes >= 1:
                quote.dislikes -= 1
        elif direction == 'decrease':
            if quote.likes >= 1:
                quote.likes -= 1
        else:
            return Response(data={'error': 'Invalid direction provided, must be one of: ["increase", "decrease"]'},
                            status=status.HTTP_400_BAD_REQUEST)

        quote.save()

        serializer = QuoteSerializer(quote)

        return Response(serializer.data)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                name='direction',
                description='Add or remove count.',
                required=True,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                enum=['increase', 'decrease'],
            ),
            OpenApiParameter(
                name='reverse_opposite',
                description='Reverse vote (remove the opposite rating).',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
            )
        ],
    )
    @action(detail=True, methods=[HTTPMethod.PATCH])
    def dislike(self, request: Request, guid: str) -> Response:
        """
        Dislike a quote.
        """
        direction = request.query_params.get('direction', 'increase')
        quote: Quote = Quote.objects.get(guid=guid)

        if direction == 'increase':
            quote.dislikes += 1

            reverse_opposite: bool = bool(strtobool(request.query_params.get('reverse_opposite', '0')))

            if reverse_opposite and quote.likes >= 1:
                quote.likes -= 1
        elif direction == 'decrease':
            if quote.dislikes >= 1:
                quote.dislikes -= 1
        else:
            return Response(data={'error': 'Invalid direction provided, must be one of: ["increase", "decrease"]'},
                            status=status.HTTP_400_BAD_REQUEST)

        quote.save()

        serializer = QuoteSerializer(quote)

        return Response(serializer.data)
