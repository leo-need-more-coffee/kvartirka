from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Article(models.Model):
    name = models.CharField(max_length=64)
    text = models.TextField()


class Comment(MPTTModel):
    article_id = models.IntegerField(null=True)
    name = models.CharField(null=True, max_length=64)
    text = models.TextField(null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
