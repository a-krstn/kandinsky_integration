from rest_framework import serializers

from .models import Article
from .tasks import get_image


class ArticleCreateSerializer(serializers.ModelSerializer):
    """
    Article Create Serializer
    """

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = ('author', 'title', 'body', 'image')
    
    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        print(bool(article.image))
        if not article.image:
            get_image.delay(article.pk)
        print(article.pk)
        return article


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Article List Serializer
    """

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'created', 'image', 'body')
