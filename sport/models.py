from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", default="default.jpg")
    job_title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Trainer(models.Model):
    title = models.CharField(max_length=150)
    picture = models.ImageField(upload_to='pics')
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    profession = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'


class Gallery(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gals')
    date_posted = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def total_likes(self):
        return self.likes.count()


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='like')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislike')
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=500)
    extra_desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news', blank=True, null=True)
    desc = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'


class EuroNews(models.Model):
    title = models.CharField(max_length=500)
    extra_desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='news', blank=True, null=True)
    desc = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'EuroNew'
        verbose_name_plural = 'EuroNews'


class Comment(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blogs = models.ForeignKey('Blog', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def __str__(self):
        return self.author.username
