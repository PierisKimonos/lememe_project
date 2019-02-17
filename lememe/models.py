from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


## from lememe.models import UserProfile, Post, Comment, Preference, Category

def get_user_image_folder(instance, filename):
    name = instance.user.username
    filename = "%s_profile_pic%s"%(name,filename[filename.find('.'):])
    return "%s/%s"%(instance.user.username,filename)

class Category(models.Model):
    max_length = 128
    user = models.ForeignKey(User)
    name = models.CharField(max_length=max_length, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category)
    # users_who_liked = models.ManyToManyField(User, through='Preference', symmetrical=True)
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date',)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    text = models.CharField(max_length=128)


class UserProfile(models.Model):
    bio_length = 200
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    bio = models.CharField(max_length=bio_length, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    joined = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to=get_user_image_folder, blank=True, verbose_name='Profile picture')

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username


class Preference(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    preference = models.BooleanField(blank=True) # True=Like, False=Dislike


## NEED TO IMPLEMENT REPORTS
