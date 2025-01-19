import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contrib.constants import POSITIVE_BIT_INTEGER_MIN, POSITIVE_BIT_INTEGER_MAX
from quotes.tests.factories import QuoteFactory, CategoryFactory


class QuotesAPITests(APITestCase):
    def test_get_random_quote(self) -> None:
        response = self.client.get(reverse(viewname='quotes-get-random-quote'))

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)

        data = response.json()

        self.assertIsInstance(obj=data, cls=dict)

        expected_keys = (
            'guid', 'created', 'modified', 'author', 'category', 'quote_text', 'image_url', 'image_alt_text', 'origin',
            'likes', 'dislikes'
        )
        for key in expected_keys:
            self.assertIn(member=key, container=data)

        author = data.get('author')
        self.assertIsInstance(obj=author, cls=dict)
        self.assertIn(member='name', container=author)
        self.assertIsInstance(obj=author.get('name'), cls=str)
        category = data.get('category')
        self.assertIsInstance(obj=category, cls=dict)
        self.assertIn(member='name', container=category)
        self.assertIsInstance(obj=category.get('name'), cls=str)
        origin = data.get('origin')
        self.assertIsInstance(obj=origin, cls=dict)
        self.assertIn(member='api_client_key', container=origin)
        self.assertIsInstance(obj=origin.get('api_client_key'), cls=str)
        self.assertIn(member='url', container=origin)
        self.assertIsInstance(obj=origin.get('url'), cls=str)
        self.assertIsInstance(obj=data.get('quote_text'), cls=str)
        self.assertIsNone(obj=data.get('image_url'))
        self.assertIsNone(obj=data.get('image_alt_text'))
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertGreaterEqual(a=likes, b=POSITIVE_BIT_INTEGER_MIN)
        self.assertLessEqual(a=likes, b=POSITIVE_BIT_INTEGER_MAX)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertGreaterEqual(a=dislikes, b=POSITIVE_BIT_INTEGER_MIN)
        self.assertLessEqual(a=dislikes, b=POSITIVE_BIT_INTEGER_MAX)

    def test_like_simple(self) -> None:
        quote = QuoteFactory(likes=0)
        response = self.client.patch(reverse(viewname='quotes-like', kwargs={'guid': quote.guid}))
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='likes', container=data)
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertEqual(first=likes, second=1)

    def test_like_reverse_possible(self):
        quote = QuoteFactory(likes=0, dislikes=1)
        response = self.client.patch(reverse(viewname='quotes-like', kwargs={'guid': quote.guid}),
                                     query_params={'reverse_opposite': True})
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='likes', container=data)
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertEqual(first=likes, second=1)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertEqual(first=dislikes, second=0)

    def test_like_reverse_impossible(self):
        quote = QuoteFactory(likes=0, dislikes=0)
        response = self.client.patch(reverse(viewname='quotes-like', kwargs={'guid': quote.guid}),
                                     query_params={'reverse_opposite': True})
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='likes', container=data)
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertEqual(first=likes, second=1)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertEqual(first=dislikes, second=0)

    def test_dislike_simple(self) -> None:
        quote = QuoteFactory(dislikes=0)
        response = self.client.patch(reverse(viewname='quotes-dislike', kwargs={'guid': quote.guid}))
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='dislikes', container=data)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertEqual(first=dislikes, second=1)

    def test_dislike_reverse_possible(self):
        quote = QuoteFactory(likes=1, dislikes=0)
        response = self.client.patch(reverse(viewname='quotes-dislike', kwargs={'guid': quote.guid}),
                                     query_params={'reverse_opposite': True})
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='likes', container=data)
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertEqual(first=likes, second=0)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertEqual(first=dislikes, second=1)

    def test_dislike_reverse_impossible(self):
        quote = QuoteFactory(likes=0, dislikes=0)
        response = self.client.patch(reverse(viewname='quotes-dislike', kwargs={'guid': quote.guid}),
                                     query_params={'reverse_opposite': True})
        data = response.json()

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)
        self.assertIn(member='likes', container=data)
        likes = data.get('likes')
        self.assertIsInstance(obj=likes, cls=int)
        self.assertEqual(first=likes, second=0)
        dislikes = data.get('dislikes')
        self.assertIsInstance(obj=dislikes, cls=int)
        self.assertEqual(first=dislikes, second=1)

    def test_get_random_quote_by_category(self) -> None:
        category = CategoryFactory(name='some-category')
        quote = QuoteFactory(category=category)
        response = self.client.get(reverse(viewname='quotes-get-random-quote-by-category'),
                                   query_params={'category': 'some-category'})

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)

        data = response.json()

        self.assertIsInstance(obj=data, cls=dict)

        expected_keys = (
            'guid', 'created', 'modified', 'author', 'category', 'quote_text', 'image_url', 'image_alt_text', 'origin',
            'likes', 'dislikes'
        )
        for key in expected_keys:
            self.assertIn(member=key, container=data)

        category = data.get('category')
        self.assertIsInstance(obj=category, cls=dict)
        self.assertIn(member='name', container=category)
        category_name = category.get('name')
        self.assertIsInstance(obj=category_name, cls=str)
        self.assertEqual(first=category_name, second='some-category')
        self.assertEqual(first=category_name, second=quote.category.name)

    def test_get_15_most_liked_quotes(self) -> None:
        # quotes = QuoteFactory.create_batch(size=15)
        response = self.client.get(reverse(viewname='quotes-get-most-liked-quotes'), query_params={'count': 15})

        self.assertEqual(first=response.status_code, second=status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(obj=data, cls=list)
        for quote in data:
            expected_keys = (
                'guid', 'created', 'modified', 'author', 'category', 'quote_text', 'image_url', 'image_alt_text',
                'origin',
                'likes', 'dislikes'
            )
            for key in expected_keys:
                self.assertIn(member=key, container=quote)

            author = quote.get('author')
            self.assertIsInstance(obj=author, cls=dict)
            self.assertIn(member='name', container=author)
            self.assertIsInstance(obj=author.get('name'), cls=str)
            category = quote.get('category')
            self.assertIsInstance(obj=category, cls=dict)
            self.assertIn(member='name', container=category)
            self.assertIsInstance(obj=category.get('name'), cls=str)
            origin = quote.get('origin')
            self.assertIsInstance(obj=origin, cls=dict)
            self.assertIn(member='api_client_key', container=origin)
            self.assertIsInstance(obj=origin.get('api_client_key'), cls=str)
            self.assertIn(member='url', container=origin)
            self.assertIsInstance(obj=origin.get('url'), cls=str)
            self.assertIsInstance(obj=quote.get('quote_text'), cls=str)
            self.assertIsNone(obj=quote.get('image_url'))
            self.assertIsNone(obj=quote.get('image_alt_text'))
            likes = quote.get('likes')
            self.assertIsInstance(obj=likes, cls=int)
            self.assertGreaterEqual(a=likes, b=POSITIVE_BIT_INTEGER_MIN)
            self.assertLessEqual(a=likes, b=POSITIVE_BIT_INTEGER_MAX)
            dislikes = quote.get('dislikes')
            self.assertIsInstance(obj=dislikes, cls=int)
            self.assertGreaterEqual(a=dislikes, b=POSITIVE_BIT_INTEGER_MIN)
            self.assertLessEqual(a=dislikes, b=POSITIVE_BIT_INTEGER_MAX)
