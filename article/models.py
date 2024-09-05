from django.db import models
from django.contrib.auth import get_user_model


class Article(models.Model):
    """
    Article class
    """

    title = models.CharField(max_length=200,
                             verbose_name='Заголовок статьи')
    body = models.TextField(max_length=5000,
                            verbose_name='Текст статьи')
    image = models.ImageField(upload_to='articles/%Y/%m/%d/',
                              blank=True,
                              null=True,
                              verbose_name='Превью',)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='articles',
                               verbose_name='Автор статьи')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.pk}. {self.title}'
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
