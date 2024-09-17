from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'image', 'created')
