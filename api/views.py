from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer


@api_view(['GET'])
def get_articles(request, id=None):
    articles = Article.objects.filter(id=id)
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


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
