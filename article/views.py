from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Article
from .serializers import ArticleCreateSerializer, ArticleListSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Article ViewSet
    """

    queryset = Article.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticleCreateSerializer
        return ArticleListSerializer
