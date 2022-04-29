from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='get', operation_description="Возвращает статью по id.", responses={200: openapi.Response('Статья.', ArticleSerializer)})
@api_view(['GET'])
def get_article(request, id=None):
    articles = Article.objects.filter(id=id)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', operation_description="Возвращает список из всех статей.", responses={200: openapi.Response('Список статей.', ArticleSerializer)})
@api_view(['GET'])
def get_all_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', operation_description="Создает статью.", responses={201: openapi.Response('Статья.', ArticleSerializer)})
@api_view(['POST'])
def add_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@swagger_auto_schema(method='get', operation_description="Получает список комментариев.", responses={200: openapi.Response('Список комментариев.', CommentSerializer)})
@api_view(['GET'])
def get_comments(request, article_id=None, comment_id=None):
    deep = int(request.query_params.get('deep', 10**9))
    if comment_id is None:
        comments = Comment.objects.filter(article_id=article_id, level__lte=deep)
    else:
        parent = Comment.objects.get(id=comment_id)
        comments = parent.get_descendants(include_self=False).filter(level__lte=deep+parent.level)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='post', operation_description="Создает комментарий.", responses={201: openapi.Response('Комментарий.', CommentSerializer)})
@api_view(['POST'])
def add_comment(request, article_id=None):
    parent = request.query_params.get('parent_id', None)
    data = request.data
    data["article_id"] = article_id
    data["parent"] = parent
    serializer = CommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
