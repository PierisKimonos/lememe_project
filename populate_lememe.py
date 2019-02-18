import os, random
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

    posts = {
        "maria": [
            {"title": "Title for post 1",
             "category": "Funny",
             "image": "maria1.jpg"},

            {"title": "Title for post 2",
             "category": "Funny",
             "image": "maria2.jpg"},

            {"title": "Title for post 3",
             "category": "Funny",
             "image": "maria3.jpg"},

        ],
        "john": [
            {"title": "Title for post 1",
             "category": "Politics",
             "image": "john1.jpg"},

            {"title": "Title for post 2",
             "category": "Politics",
             "image": "john2.jpg"},

            {"title": "Title for post 3",
             "category": "Politics",
             "image": "john3.jpg"},
        ],
    }

    users = {"maria": {"password": "1111",
                       "firstname": "Maria",
                       "surname": "Smith",
                       "bio": "Maria's Bio.",
                       "email": "maria1234@lememe.com",
                       "website": "www.maria1234.com",
                       "posts": posts["maria"],
                       # "comments": maria_comments,
                       },
             "john": {"password": "1111",
                      "firstname": "John",
                      "surname": "McDonald",
                      "bio": "John's Bio.",
                      "email": "john1234@lememe.com",
                      "website": "www.john1234.com",
                      "posts": posts["john"],
                      # "comments": john_comments,
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
    # 2. Categories
    # 3. UserProfiles
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
                     user_data["firstname"],
                     user_data["surname"],
                     user_data["bio"],
                     user_data["email"],
                     user_data["website"])
        # need to add posts and then comments
        for post in posts[user]:
            # If the category does not exist, allow the user to create it
            category = Category.objects.get(name=post["category"])
            p = add_post(u,
                         category,
                         post["title"],
                         post["image"])

    # add 50 random comments to random posts as random existing users
    numOfComments = 50
    for i in range(1, numOfComments + 1):
        if Comment.objects.filter(id=i).count() == 0:
            user = random.choice(User.objects.all())
            post = random.choice(Post.objects.all())
            c = add_comment(user=user,post=post, text=generateHaHaComment())


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


def add_user(username, password, firstname, surname, bio, email, website):
    user = User.objects.get_or_create(username=username, first_name=firstname, last_name=surname, email=email)[0]
    u = UserProfile.objects.get_or_create(user=user)[0]
    # u.first_name = firstname
    # u.last_name = surname
    u.password = password
    if u.picture.name != "%s.jpg"%username:
        image_path = os.path.join(PROJECT_DIR, 'population_images','profiles','%s.jpg'%username)
        u.picture.save("%s.jpg"%username, File(open(image_path, 'rb')))
    u.bio = bio
    # u.email = email
    u.website = website
    u.joined = datetime.now()
    u.save()
    return user


def add_category(user, name, views=0):
    c = Category.objects.get_or_create(name=name, user=user)[0]
    c.views = views
    c.save()
    return c

# posts(User, Category, title, date)
def add_post(user, category, title, image_name):
    p = Post.objects.get_or_create(title=title, user=user, category=category)[0]
    image_path = os.path.join(PROJECT_DIR, 'population_images', 'posts', image_name)
    p.image.save(image_name, File(open(image_path, 'rb')))
    p.save()
    return p


def add_comment(user, post, text):
    c = Comment.objects.create(user=user, post=post)
    c.text = text
    c.save()
    return c


def generateHaHaComment():
    hahas = ["ha", "hahaha", "hahahahaha", "lol", "omg"]
    comment = []
    for i in range(10):
        comment.append(random.choice(hahas))
    return " ".join(comment)


# Start execution here!
if __name__ == '__main__':
    print("Starting Lememe population script...")
    populate()
