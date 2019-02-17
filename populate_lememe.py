import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lememe_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from django.core.files import File
from lememe.models import UserProfile, Post, Comment, Preference, Category

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def populate():
    # Superuser is used to create the initial categories
    superuser = create_superuser("god", "1111")

    categories = {
        "Funny": {"views": 128},
        "Animals": {"views": 128},
        "Legends": {"views": 128},
        "Awesome": {"views": 128},
        "Basketball": {"views": 128},
        "Car": {"views": 128},
        "Cosplay": {"views": 128},
        "Art": {"views": 128},
        "Football": {"views": 128},
        "Gaming": {"views": 128},
        "History": {"views": 128},
        "Horror": {"views": 128},
        "Family": {"views": 128},
        "Movie": {"views": 128},
        "Music": {"views": 128},
        "Kids": {"views": 128},
        "Tech": {"views": 128},
        "Politics": {"views": 128},
        "Relationship": {"views": 128},
        "Roast": {"views": 128},
        "Savage": {"views": 128},
        "School": {"views": 128},
        "Sport": {"views": 128},}

    users = {"maria": {"password": "1111",
                       "bio": "Maria's Bio.",
                       "email": "maria1234@lememe.com",
                       "website": "www.maria1234.com",
                       # "comments": maria_comments,
                       # "posts": maria_posts,
                       },
             "John": {"password": "1111",
                      "bio": "John's Bio.",
                      "email": "john1234@lememe.com",
                      "website": "www.john1234.com",
                      # "comments": john_comments,
                      # "posts": john_posts,
                      }
             }


    #
    # comments = [
    #     {"maria": {"password": "1111",
    #                "bio": "Maria's Bio.",
    #                "email": "maria1234@lememe.com",
    #                "website": "www.maria1234.com",
    #                "categories": maria_comments,
    #                "posts": maria_posts, },
    #      "John": {"password": "1111",
    #               "bio": "John's Bio.",
    #               "email": "john1234@lememe.com",
    #               "website": "www.john1234.com",
    #               "categories": john_comments,
    #               "posts": john_posts, }
    #      }
    # ]

    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/",
         "views": 1},

        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 1
         },

        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 1}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": 1},

        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 1},

        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": 1}]

    other_pages = [
        {"title": "Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views": 1},

        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 1}]

    # ----------------------------------------------------
    # ENTITIES
    # posts(User, Category, title, date, likes, dislikes)
    # User (username, password, picture, bio, e-mail, website, joined, Favorites, Meme page)
    # Category (User, name, views)
    # Report(User, Post, date)
    # Preference(User, Post, preference)
    # Comment(User, Post, date, text)
    # ----------------------------------------------------

    # ----------------------------------------------------
    # Order in which entities have to be created:
    # 1. Superuser
    # 2. UserProfiles
    # 3. Categories
    # 4. Posts
    # 5. Comments
    # ----------------------------------------------------

    for cat in sorted(categories.keys()):
        cat_data = categories.get(cat)
        c = add_category(user=superuser, name=cat, views=cat_data["views"])
        # for p in cat_data["pages"]:
        #     add_page(c, p["title"], p["url"], p["views"])

    for user, user_data in users.items():
        u = add_user(user,
                     user_data["password"],
                     user_data["bio"],
                     user_data["email"],
                     user_data["website"])
        # need to add posts and then comments


    # # Print out the categories we have added.
    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print("- {0} - {1}".format(str(c), str(p)))


def create_superuser(username, password):
    superuser = User.objects.get_or_create(username=username)[0]
    superuser.set_password(password)
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    return superuser


def add_user(username, password, bio, email, website):
    user = User.objects.get_or_create(username=username)[0]
    u = UserProfile.objects.get_or_create(user=user)[0]
    u.password = password
    image_path = os.path.join(PROJECT_DIR, 'population_images','profiles','%s.jpg'%username)
    upload_path = os.path.join(PROJECT_DIR, 'media','%s'%username)
    u.picture.save("%s.jpg"%username, File(open(image_path, 'rb')))
    u.bio = bio
    u.email = email
    u.website = website
    u.joined = datetime.now()
    u.save()
    return u


def add_category(user, name, views=0):
    c = Category.objects.get_or_create(name=name, user=user)[0]
    c.views = views
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
