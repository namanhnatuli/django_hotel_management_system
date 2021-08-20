import json
import operator

from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from functools import reduce

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from dateutil import parser
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from blog.models import Article, Category, Comment
from blog.forms import CategoryForm, ArticleCreateForm, ArticleUpdateForm
from dashboard.models import Profile

from reservation.forms import ReservationForm
from reservation.models import Reservation


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_category'
    template_name = 'category_form.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_category'
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_category'
    model = Category
    form_class = CategoryForm
    template_name = 'category_update.html'
    success_url = reverse_lazy('category_list')


class DashboardArticleListView(LoginRequiredMixin, ListView):
    permission_required = 'blog.view_article'
    model = Article
    template_name = 'dashboard_article_list.html'


class DashboardArticleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'blog.view_article'
    model = Article
    template_name = 'article_detail.html'


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_article'
    template_name = 'article_form.html'
    model = Article
    form_class = ArticleCreateForm
    success_url = reverse_lazy('dashboard_article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == "PUBLISHED":
            form.instance.published = True
            form.instance.date_published = timezone.now()
            form.save()
        return super(ArticleCreateView, self).form_valid(form)


def CategoryCreatePopup(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "category_form_popup.html", {"form": form})


@csrf_exempt
def get_category_id(request):
    if request.is_ajax():
        category_name = request.GET['name']
        category_id = Category.objects.get(name=category_name).id
        data = {'category_id': category_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_article'
    model = Article
    template_name = 'article_confirm_delete.html'
    success_url = reverse_lazy('dashboard_article_list')


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_article'
    model = Article
    form_class = ArticleUpdateForm
    template_name = 'article_update.html'
    success_url = reverse_lazy('dashboard_article_list')

    def form_valid(self, form):
        if form.instance.published == False and form.instance.status == "PUBLISHED":
            form.instance.published = True
            form.instance.date_published = timezone.now()
            form.save()
        return super(ArticleUpdateView, self).form_valid(form)


class UserArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'user_articles.html'

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


def reservationrequest(request):
    if request.method == "POST":
        guestname = request.POST['guestname']
        phone = request.POST['phone']
        email = request.POST['email']
        adult = request.POST['adult']
        child = request.POST['child']
        arrivetime = request.POST['arrivetime']
        departuretime = request.POST['departuretime']
        if parser.parse(arrivetime) < timezone.now():
            messages.error(request, 'Ngay du kien den khong hop le')
        elif departuretime < arrivetime:
            messages.error(request, 'Ngay du kien di khong hop le')
        else:
            r = Reservation.objects.create(guest_name=guestname, guest_phone=phone, guest_email=email,
                                           no_of_children=child, no_of_adults=adult,
                                           expected_arrival_date_time=arrivetime,
                                           expected_departure_date_time=departuretime)
            r.save()
            messages.success(request, "Dat truoc thanh cong", extra_tags='green')
    return render(request, 'blog/home.html')


class ReservationCreateView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'blog/home.html'
    success_url = reverse_lazy('blog_home')
    success_message = 'Dat lich thanh cong'

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class BlogRoomListView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'blog/rooms.html'
    success_url = reverse_lazy('blog_room')
    success_message = 'Dat lich thanh cong'

    def get_context_data(self, **kwargs):
        context = super(BlogRoomListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class AboutView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'blog/about.html'
    success_url = reverse_lazy('blog_about')
    success_message = 'Dat lich thanh cong'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class ContactView(SuccessMessageMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('blog_contact')
    success_message = 'Dat lich thanh cong'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context


class BlogArticleListView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'blog/blog_article_list.html'
    success_url = reverse_lazy('blog_article_list')
    success_message = 'Dat lich thanh cong'

    def get_context_data(self, **kwargs):
        context = super(BlogArticleListView, self).get_context_data(**kwargs)
        article_list = Article.objects.filter(status=Article.PUBLISHED)
        paginator = Paginator(article_list, 3)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['article_list'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['categories'] = Category.objects.filter(approved=True)
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context


class BlogCategoryDetailView(FormMixin, DetailView):
    model = Category
    form_class = ReservationForm
    template_name = 'blog/blog_category_detail.html'

    def get_success_url(self):
        return reverse('blog_category_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(BlogCategoryDetailView, self).get_context_data(**kwargs)
        article_list = Article.objects.filter(status=Article.PUBLISHED, category=self.object)
        paginator = Paginator(article_list, 6)
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        context['article_list'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['form'] = self.get_form()
        context['categories'] = Category.objects.filter(approved=True)
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Dat lich thanh cong')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(BlogCategoryDetailView, self).form_valid(form)


class BlogTagDetailView(FormMixin, DetailView):
    model = Tag
    form_class = ReservationForm
    template_name = 'blog/blog_tag_detail.html'

    def get_success_url(self):
        return reverse('blog_tag_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(BlogTagDetailView, self).get_context_data(**kwargs)
        article_list = Article.objects.filter(tags__slug=self.object.slug)
        paginator = Paginator(article_list, 6)
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        context['article_list'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['form'] = self.get_form()
        context['categories'] = Category.objects.filter(approved=True)
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Dat lich thanh cong')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(BlogTagDetailView, self).form_valid(form)


class BlogArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'blog/blog_article_detail.html'
    form_class = ReservationForm

    def get_success_url(self):
        return reverse('blog_article_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        context = super(BlogArticleDetailView, self).get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        context['next_article'] = Article.objects.filter(status=Article.PUBLISHED, date_published__gt=article.date_published).order_by('date_published').first()
        context['previous_article'] = Article.objects.filter(status=Article.PUBLISHED, date_published__lt=article.date_published).order_by('-date_published').first()
        context['author'] = Profile.objects.get_or_create(user=article.author)
        context['form'] = self.get_form()
        context['categories'] = Category.objects.filter(approved=True)
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Dat lich thanh cong')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(BlogArticleDetailView, self).form_valid(form)


def send_comment(request, slug):
    if request.method == "POST":
        comment = request.POST.get('comment')
        name = request.POST.get('name')
        email = request.POST.get('email')
        article = Article.objects.get(slug=slug)
        Comment.objects.create(name=name, email=email, comment=comment, article=article)
    return HttpResponseRedirect(reverse_lazy('blog_article_detail', kwargs={'slug': slug}))


class AuthorArticlesListView(FormMixin, DetailView):
    model = User
    template_name = 'blog/blog_author_articles.html'
    form_class = ReservationForm

    def get_success_url(self):
        return reverse('blog_author_articles', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AuthorArticlesListView, self).get_context_data(**kwargs)
        article_list = Article.objects.filter(author=self.object.pk)
        paginator = Paginator(article_list, 6)
        page = self.request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        context['article_list'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['form'] = self.get_form()
        context['categories'] = Category.objects.filter(approved=True)
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Dat lich thanh cong')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(AuthorArticlesListView, self).form_valid(form)


class ArticleSearchListView(ListView):
    model = Article
    template_name = "blog/article_search_list.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            title_search = Article.objects.filter(
                reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(slug__icontains=q) for q in query_list))
            )
            tag_search = Article.objects.filter(reduce(operator.and_, (Q(tags__slug__icontains=q) for q in query_list)))
            article_results = title_search | tag_search
            search_results = article_results.filter(status=Article.PUBLISHED).distinct()
            return search_results
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        context['query'] = self.request.GET.get('q')
        context['recent_post'] = Article.objects.filter(status=Article.PUBLISHED).order_by('-date_published')[:4]
        return context


