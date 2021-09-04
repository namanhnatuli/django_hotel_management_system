# Third party imports.
from rest_framework import serializers

# Local application imports
from blog.models import Article, Category, Comment


class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source="category.name")
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Article
        fields = ["title", "slug", "author", "category", "image", "body", "status"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "name", "email", "article", "comment", "date_created", "date_updated", "approved"]
        read_only_fields = ['approved']


class CommentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
