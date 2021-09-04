# Django imports
from django import forms
from django.forms import TextInput, Select, FileInput

# Third-party app imports
from ckeditor.fields import RichTextFormField
from taggit.forms import TagWidget, TagField
# Blog app imports
from blog.models import Article, Category, Comment


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "approved"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ArticleCreateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(approved=True), widget=forms.Select())
    body = RichTextFormField()

    class Meta:
        model = Article
        fields = ["title", "category", "image", "body", "tags", "status"]
        widgets = {
            'title': TextInput(attrs={'name': "article-title", 'class': "form-control", 'id': "articleTitle"}),
            'image': FileInput(attrs={"class": "clearablefileinput", "type": "file", "id": "articleImage", "name": "article-image"}),
            'tags': TextInput(attrs={'name': "tags", 'data-role': "tagsinput", 'placeholder': "Example: sports, game"}),
            'status': Select(),
        }


class ArticleUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.filter(approved=True), widget=forms.Select())
    tags = TagField(widget=TagWidget(attrs={'name': "tags", 'placeholder': "Example: sports, game", 'id': "tags", 'data-role': "tagsinput"}))
    body = RichTextFormField()

    class Meta:
        model = Article
        fields = ["title", "category", "image", "body", "tags", "status"]
        widgets = {
            'title': TextInput(attrs={'name': "article-title", 'class': "form-control", 'id': "articleTitle"}),
            'image': FileInput(attrs={"class": "clearablefileinput", "type": "file", "id": "articleImage","name": "article-image"}),
            'status': Select(),
        }


class CommentUpdateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['approved']
