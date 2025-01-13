from rest_framework import serializers

from quotes.models import Author, Category, Quote


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class QuoteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()

    class Meta:
        model = Quote
        fields = ['guid', 'created', 'modified', 'author', 'category', 'quote_text', 'image_url', 'image_alt_text',
                  'origin', 'likes', 'dislikes']
