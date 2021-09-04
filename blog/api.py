from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

from blog.models import Category, Article, Comment
from blog.serializers import CategorySerializer, ArticleSerializer, CommentCreateSerializer, CommentConfigSerializer
from django_hotel_management_system.permissions import IsOwner


class ArticleList(generics.ListAPIView):
    queryset = Article.objects.filter(status='PUBLISHED')
    serializer_class = ArticleSerializer


class CategoryArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        articles = Article.objects.filter(category__slug=slug, status='PUBLISHED')
        return articles


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class ArticleCommentList(generics.ListCreateAPIView):
    serializer_class = CommentCreateSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        comments = Comment.objects.filter(article__slug=slug, approved=True)
        return comments


class CommentList(generics.ListAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Comment.objects.all()
    serializer_class = CommentConfigSerializer


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Comment.objects.all()
    serializer_class = CommentConfigSerializer
