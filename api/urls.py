from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.add_article),
    path('articles/<int:id>', views.get_article),
    path('articles/all', views.get_all_articles),

    path('articles/<int:article_id>/comments/', views.add_comment),
    path('articles/<int:article_id>/comments/all', views.get_comments),
    path('articles/<int:article_id>/comments/<int:comment_id>', views.get_comments),
]