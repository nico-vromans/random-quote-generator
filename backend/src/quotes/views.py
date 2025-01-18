from http import HTTPMethod

from distutils.util import strtobool
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from contrib.views import GenericGUIDViewSet
from .models import Quote
from .serializers import QuoteSerializer
from .utils.quote_fetching import fetch_random_quote, fetch_random_quote_from_database


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
        quote: Quote | None = fetch_random_quote()

        if quote is None:
            return Response(data='No quotes found', status=status.HTTP_404_NOT_FOUND)

        serializer = QuoteSerializer(instance=quote)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

        serializer = QuoteSerializer(instance=quote)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

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

        serializer = QuoteSerializer(instance=quote)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                name='category',
                description='Category of the quote to find.',
                required=True,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
            ),
        ],
    )
    @action(detail=False, methods=[HTTPMethod.GET])
    def get_random_quote_by_category(self, request: Request) -> Response:
        """
        Get a random quote from the database, with given category.
        """
        category: str = request.query_params.get('category')
        quote: Quote = fetch_random_quote_from_database(category=category)

        serializer = QuoteSerializer(instance=quote)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        parameters=[
            OpenApiParameter(
                name='count',
                description='How many quotes to return (optional, default=10).',
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT,
                default=10,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=QuoteSerializer(many=True),
                description='Get a list of the X most liked quotes.',
            )
        },
    )
    @action(detail=False, methods=[HTTPMethod.GET])
    def get_most_liked_quotes(self, request: Request) -> Response:
        quote_count: int = request.query_params.get('count', 10)
        most_liked_quotes: QuerySet = Quote.objects.order_by('-likes')[:int(quote_count)]
        serializer = QuoteSerializer(instance=most_liked_quotes, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
