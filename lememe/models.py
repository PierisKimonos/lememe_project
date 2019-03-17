import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import IntegrityError
from lememe.storage import OverwriteStorage


def get_user_image_folder(instance, filename):
    name = instance.user.username
    filename = "%s_profile_pic%s"%(name,filename[filename.find('.'):])
    return "%s/%s"%(instance.user.username,filename)


def get_post_image_folder(instance, filename):
    return "%s/post/%s"%(instance.user.username,instance.client_id)


def get_category_image_folder(instance, filename):
    # the name of the file will be the category name with the format (ie. Funny.jpg)
    filename = instance.name + filename[filename.rfind('.'):]
    return "_category_pictures/%s"%filename


class Category(models.Model):
    max_length = 128
    user = models.ForeignKey(User)
    name = models.CharField(max_length=max_length, unique=True)
    views = models.IntegerField(default=0)
    picture = models.ImageField(storage=OverwriteStorage(),upload_to=get_category_image_folder, blank=True, verbose_name="Category Picture")
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __eq__(self, other):
        try:
            return self.name == other.name # other might be of type None
        except:
            return False

class Post(models.Model):
    client_id = models.CharField(primary_key=False,max_length=8,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    image = models.ImageField(storage=OverwriteStorage(),upload_to=get_post_image_folder, blank=True, verbose_name="Image")
    views = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.client_id:
            super(Post, self).save(*args, **kwargs)
            return

        newid = uuid.uuid4().hex[:8]
        while Post.objects.filter(client_id=newid).count() != 0:
            newid = uuid.uuid4().hex[:8]

        self.client_id = newid
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('date',)

    def get_total_preferences(self):
        return Preference.objects.filter(post=self).count()

    def get_rating(self):
        total_ratings = self.get_total_preferences()
        if total_ratings == 0:
            return 0
        else:
            likes = Preference.objects.filter(post=self, liked=True).count()
            return likes / total_ratings * 100

    def get_num_of_comments(self):
        return Comment.objects.filter(post=self).count()

    def increament_view_count(self):
        self.views = self.views + 1
        self.save()



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
    website = models.URLField(blank=True)
    picture = models.ImageField(storage=OverwriteStorage(),upload_to=get_user_image_folder, blank=True, verbose_name='Profile picture')

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(blank=True) # True=Like, False=Dislike


## NEED TO IMPLEMENT REPORTS
