from rest_framework import serializers

from .models import Article


class ArticleCreateSerializer(serializers.ModelSerializer):
    """
    Article Create Serializer
    """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = ('author', 'title', 'body', 'image')


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Article List Serializer
    """

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'created', 'image', 'body')
