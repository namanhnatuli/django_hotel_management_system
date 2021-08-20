from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField('Chuyen muc', max_length=100, null=False, blank=False, unique=True, error_messages={'unique': "Chuyen muc da ton tai"})
    slug = models.SlugField()
    approved = models.BooleanField('Phe duyet', default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)


class Article(models.Model):
    # Article status constants
    DRAFTED = "DRAFTED"
    PUBLISHED = "PUBLISHED"
    HIDDEN = "HIDDEN"

    # CHOICES
    STATUS_CHOICES = (
        (DRAFTED, 'Ban thao'),
        (PUBLISHED, 'Dang tai'),
        (HIDDEN, 'An'),
    )

    # BLOG MODEL FIELDS
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(default='slider/img-slide-7.jpg', upload_to='blog')
    body = RichTextUploadingField(blank=True)
    tags = TaggableManager(blank=True)
    date_published = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        unique_together = ("title",)
        ordering = ('-date_published',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=False)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):

    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField()
    comment = models.TextField(null=False, blank=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Comment by {self.name} on {self.article}"
