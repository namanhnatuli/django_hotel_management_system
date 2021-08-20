from django.urls import path
from blog import views

urlpatterns = [
    path('category/list', views.CategoryListView.as_view(), name='category_list'),
    path('category/create', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<slug:slug>/update', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<slug:slug>/delete', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('', views.ReservationCreateView.as_view(), name='blog_home'),
    path('room', views.BlogRoomListView.as_view(), name='blog_room'),
    path('about', views.AboutView.as_view(), name='blog_about'),
    path('contact', views.ContactView.as_view(), name='blog_contact'),
    path('articles', views.BlogArticleListView.as_view(), name='blog_article_list'),
    path('<slug:slug>', views.BlogArticleDetailView.as_view(), name='blog_article_detail'),
    path('category/<slug:slug>', views.BlogCategoryDetailView.as_view(), name='blog_category_detail'),
    path('<slug:slug>/send-comment', views.send_comment, name='blog_send_comment'),
    path('tag/<slug:slug>', views.BlogTagDetailView.as_view(), name='blog_tag_detail'),
    path('articles/search', views.ArticleSearchListView.as_view(), name='article_search_list_view'),
    path('author/<int:pk>', views.AuthorArticlesListView.as_view(), name='blog_author_articles'),

    path('article/<slug:slug>', views.DashboardArticleDetailView.as_view(), name='dashboard_article_detail'),
    path('article/list/', views.DashboardArticleListView.as_view(), name='dashboard_article_list'),
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<slug:slug>/update', views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<slug:slug>/delete', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('myarticle/', views.UserArticlesListView.as_view(), name='my_articles'),

    path('article/category/create', views.CategoryCreatePopup, name="category_create_popup"),
    path('article/category/ajax/get_category_id', views.get_category_id, name="get_customer_id"),
]