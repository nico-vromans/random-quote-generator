from rest_framework import serializers

from quotes.models import Author, Category, Quote, QuoteOrigin


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class QuoteOriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteOrigin
        fields = ('url',)


class QuoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    origin = QuoteOriginSerializer()

    class Meta:
        model = Quote
        fields = ['guid', 'created', 'modified', 'author', 'category', 'quote_text', 'image_url', 'image_alt_text',
                  'origin', 'likes', 'dislikes']
