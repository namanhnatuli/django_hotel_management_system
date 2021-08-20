from django.contrib import admin

from blog import models
# Register your models here.

admin.site.register(models.Category)


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_published', 'published', 'status', 'views')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'date_created')
