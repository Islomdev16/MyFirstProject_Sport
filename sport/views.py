from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import *
import math
from django.urls import reverse, reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.db.models import F

# from django.views.generic import ListView, DetailView

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    profiles = Profile.objects.all().order_by('-id')
    context = {
        'profiles':profiles,
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'profile.html', context)


def home(request):
    gallery_home = Gallery.objects.all().order_by('-date_posted')[:18]
    blog_home = Blog.objects.all().order_by('-created_at')[:3]
    newslg = News.objects.all().order_by('-date_posted')[:1]
    news = News.objects.all().order_by('-date_posted')[1:7]

    paginator = Paginator(gallery_home, 6)
    page_number = request.GET.get('page')
    gallery_home = paginator.get_page(page_number)

    context = {
        'gallery_home': gallery_home,
        'blog_home': blog_home,
        'newslg':newslg,
        'news':news
    }
    return render(request, 'home.html', context)



def about(request):
    news_about = News.objects.all().order_by('-date_posted')[:3]

    return render(request, 'about.html', {'news_about': news_about})


def gallery(request):
    galleries = Trainer.objects.all().order_by('-date_posted')[:5]
    sporters = Gallery.objects.all().order_by('-date_posted')

    paginator = Paginator(sporters, 6, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'galleries': galleries,
        'page_obj': page_obj
    }
    return render(request, 'gallery.html', context)


def gallery_detail(request, id):
    sporter = Gallery.objects.get(pk=id)
    context = {
        'sporter':sporter
    }
    return render(request, 'gallery_detail.html', context)


def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')

    paginator = Paginator(blogs, 9, orphans=1)
    page_number = request.GET.get('page')
    blog_obj = paginator.get_page(page_number)

    # The Second Method for Creating pagination Starting Point

    # no_of_posts = 9
    # page = request.GET.get('page')
    # if page is None:
    #     page=1
    # else:
    #     page = int(page)

    # blog_obj = Blog.objects.all().order_by('-created_at')
    # length = len(blog_obj)
    # blog_obj = blog_obj[(page-1)*no_of_posts: page*no_of_posts]
    # if page > 1:
    #     prev = page - 1
    # else:
    #     prev = None

    # if page < math.ceil(length / no_of_posts):
    #     nxt = page + 1
    # else:
    #     nxt = None

    # The Second Method for Creating pagination Ending Point


    context={
        'blog_obj':blog_obj,
    }
    return render(request, 'blog.html', context)


def search_blog(request):
    valueb = request.POST.get('search_blog')
    blog_obj = Blog.objects.filter(title__icontains=valueb)
    context = {
        'blog_obj': blog_obj
    }
    return render(request, 'blog.html', context)


def blog_pre(request):
    latest_blogs = Blog.objects.all().order_by('-created_at')[:3]
    context={
        'latest_blogs':latest_blogs
    }
    return render(request, 'single_blog_pre.html', context)

# def add_comment(request, pk):
#     blog = get_object_or_404(Blog, pk=id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.blog = blog
#             comment.save()
#             return redirect('blog_detail', pk=blog.id)
#     else:
#         form = CommentForm()
#     context = {'form': form}
#
#     return render(request, 'blog_detail', context)


def blog_detail(request, id, *args, **kwargs):
    blog = Blog.objects.get(pk=id)
    if request.user != blog.user:
        blog.views = F("views") + 1
        blog.save()
        blog.refresh_from_db()

    form = CommentForm(request.POST)
    comments = Comment.objects.filter(blogs=blog).order_by('-created_on')
    comments_count = Comment.objects.filter(blogs=blog).count()

    # if form.is_valid():
    #     new_comment = form.save(commit=False)
    #     new_comment.author = request.user
    #     new_comment.blog = blog
    #     new_comment.save()
    # return HttpResponseRedirect(reverse_lazy('blog_detail'))


    blog = Blog.objects.get(pk=id)
    latest_blogs = Blog.objects.all().order_by('-created_at')[:3]
    context={
        'blog':blog,
        'latest_blogs':latest_blogs,
        'comments':comments,
        'form':form,
        'comments_count':comments_count
    }
    return render(request, 'single_blog.html', context)

    # def post(self, request, pk, *args, **kwargs):
    #     blog = Blog.objects.get(pk=pk)
    #     form = CommentForm(request.POST)
    #     comments_count = Comment.objects.filter(blogs=blog).count()
    #
    #     if form.is_valid():
    #         new_comment = form.save(commit=False)
    #         new_comment.author = request.user
    #         new_comment.blog = blog
    #         new_comment.save()
    #
    #         # comments = Comment.objects.filter(blogs=blog).order_by('-created_on')
    #
    #     context = {
    #         'blog':blog,
    #         'form':form,
    #         'comments_count':comments_count,
    #         # 'blog':blog,
    #         # 'latest_blogs':latest_blogs,
    #     }
    #     return HttpResponseRedirect(reverse_lazy('blog_detail'))
        # return render(request, 'single_blog.html', context)

# class BlogComment(LoginRequiredMixin, View):
#     def post(self, request, pk, *args, **kwargs):
#         blog = Blog.objects.get(pk=pk)
#         form = CommentForm(request.POST)
#         comments_count = Comment.objects.filter(blogs=blog).count()
#
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.blog = blog
#             new_comment.save()
#
#             comments = Comment.objects.filter(blogs=blog).order_by('-created_on')
#
#         context = {
#             'blog':blog,
#             'form':form,
#             'comments_count':comments_count,
#         }
#         return HttpResponseRedirect(reverse_lazy('blog_detail'))
#         # return render(request, 'single_blog.html', context)



def news(request):
    eunews = EuroNews.objects.all().order_by('-date_posted')
    title_news = EuroNews.objects.all().order_by('date_posted')[:8]

    paginator = Paginator(eunews, 9, orphans=1)
    page_number = request.GET.get('page')
    eunews_obj = paginator.get_page(page_number)

    news = News.objects.all().order_by('-date_posted')

    paginator = Paginator(news, 9, orphans=1)
    page_number = request.GET.get('page')
    news_obj = paginator.get_page(page_number)

    context = {
        'news_obj':news_obj,
        'eunews_obj':eunews_obj,
        'title_news':title_news
    }
    return render(request, 'news.html', context)


def search_news(request):
    valuen = request.POST.get('search_news')
    news_obj = News.objects.filter(title__contains=valuen)
    eunews_obj = EuroNews.objects.filter(title__contains=valuen)

    context = {
        'news_obj': news_obj,
        'eunews_obj':eunews_obj
    }
    return render(request, 'news.html', context)


def news_detail(request, id):
    new = News.objects.get(pk=id)
    if request.user != new.user:
        new.views = F("views") + 1
        new.save()
        new.refresh_from_db()

    new = News.objects.get(pk=id)
    latest_news = News.objects.all().order_by('-date_posted')[:5]
    context={
        'new':new,
        'latest_news':latest_news
    }
    return render(request, 'single_news.html', context)


def eunews_detail(request, id):
    eunew = EuroNews.objects.get(pk=id)
    latest_eunews = EuroNews.objects.all().order_by('-date_posted')[:5]
    context={
        'eunew':eunew,
        'latest_eunews':latest_eunews
    }
    return render(request, 'single_eunews.html', context)


def trainers(request):
    trainers = Trainer.objects.all().order_by('-date_posted')
    context = {
        'trainers':trainers,
    }
    return render(request, 'trainers.html', context)


# Authorization Backend Section

def register(request):
    if request.method == 'POST':
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username you entered already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email you entered already taken!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, 'Not password matching!')
            return redirect('register')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password1']

        user = auth.authenticate(username=username1, password=password1)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect("home")


def like_gallery(request, pk):
    sporter = get_object_or_404(Gallery, id=request.POST.get('gallery_id'))
    if request.user in sporter.likes.all():
        sporter.likes.remove(request.user)
        sporter.dislikes.add(request.user)
    else:
        sporter.likes.add(request.user)
        sporter.dislikes.remove(request.user)
    return redirect('gallery')


def dislike_gallery(request, pk):
    sporter = get_object_or_404(Gallery, id=request.POST.get('disgallery_id'))
    if request.user in sporter.dislikes.all():
        sporter.likes.add(request.user)
        sporter.dislikes.remove(request.user)
    else:
        sporter.likes.remove(request.user)
        sporter.dislikes.add(request.user)
    return redirect('gallery')

def like_blog(request, pk):
    blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        blog.dislikes.add(request.user)
    else:
        blog.likes.add(request.user)
        blog.dislikes.remove(request.user)
    return redirect('blog')


def dislike_blog(request, pk):
    blog = get_object_or_404(Blog, id=request.POST.get('disblog_id'))
    if request.user in blog.dislikes.all():
        blog.likes.add(request.user)
        blog.dislikes.remove(request.user)
    else:
        blog.likes.remove(request.user)
        blog.dislikes.add(request.user)
    return redirect('blog')

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('comment_like', '/')
        return HttpResponseRedirect(next)

class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('comment_dislike', '/')
        return HttpResponseRedirect(next)
