from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:id>/', views.gallery_detail, name='gallery_detail'),
    path('like/<int:pk>/', views.like_gallery, name='like_gallery'),
    path('dislike/<int:pk>/', views.dislike_gallery, name='dislike_gallery'),

    # blog and blog_detail section
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    # path('blog/comment/<int:pk>/', views.BlogComment.as_view(), name='blog-comment'),

    path('blog/single_blog_pre/', views.blog_pre, name="single_blog_pre"),
    path('blog/search_blog/', views.search_blog, name='search_blog'),
    path('blog/like/<int:pk>/', views.like_blog, name='like_blog'),
    path('blog/dislike/<int:pk>/', views.dislike_blog, name='dislike_blog'),
    path('blog/<int:blog_pk>/comment/<int:pk>/like', views.AddCommentLike.as_view(), name='comment-like'),
    path('blog/<int:blog_pk>/comment/<int:pk>/dislike', views.AddCommentDislike.as_view(), name='comment-dislike'),

    # path('blog/<int:pk>/<int:pk>/', views.CommentLike, name='comment-like'),
    # news and news_detail section
    path('news/', views.news, name='news'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('eunews/<int:id>/', views.eunews_detail, name='eunews_detail'),
    path('news/search_news/', views.search_news, name='search_news'),

    path('trainers/', views.trainers, name='trainers'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
