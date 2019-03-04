import os, random
from parse_population_files import *
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lememe_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.files import File
from lememe.models import UserProfile, Post, Comment, Preference, Category

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def populate():
    # Superuser is used to create the initial categories
    superuser = create_superuser("god", "1111")

    categories = parseCatrgories(os.path.join("population_files","categories.csv"))
    # categories = [
    #     "Funny",
    #     "Animals",
    #     "Legends",
    #     "Awesome",
    #     "Basketball",
    #     "Car",
    #     "Cosplay",
    #     "Art",
    #     "Football",
    #     "Gaming",
    #     "History",
    #     "Horror",
    #     "Family",
    #     "Movie",
    #     "Music",
    #     "Kids",
    #     "Tech",
    #     "Politics",
    #     "Relationship",
    #     "Roast",
    #     "Savage",
    #     "School",
    #     "Sport",
    # ]

    posts = parsePosts(os.path.join("population_files","posts.csv"))
    # posts = {
    #     "maria": [
    #         {"title": "Title for post 1",
    #          "category": "Funny",
    #          "image": "maria1.jpg"},
    #
    #         {"title": "Title for post 2",
    #          "category": "Funny",
    #          "image": "maria2.jpg"},
    #
    #         {"title": "Title for post 3",
    #          "category": "Funny",
    #          "image": "maria3.jpg"},
    #
    #     ],
    #     "john": [
    #         {"title": "Title for post 1",
    #          "category": "Politics",
    #          "image": "john1.jpg"},
    #
    #         {"title": "Title for post 2",
    #          "category": "Politics",
    #          "image": "john2.jpg"},
    #
    #         {"title": "Title for post 3",
    #          "category": "Politics",
    #          "image": "john3.jpg"},
    #     ],
    # }

    users = parseUsers(os.path.join("population_files","users.csv"))

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

    for cat in sorted(categories,key=lambda x: x[0]):  # sort the categories by name
        c = add_category(user=superuser, name=cat[0], image_name=cat[1])
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
        for post in posts.get(user,[]):
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


# def add_user(username, password, firstname, surname, bio, email, website):
#     user = User.objects.get_or_create(username=username, first_name=firstname, last_name=surname, email=email)[0]
#     u = UserProfile.objects.get_or_create(user=user)[0]
#     # u.first_name = firstname
#     # u.last_name = surname
#     u.password = password
#     if u.picture.name != "%s.jpg"%username:
#         image_path = os.path.join(PROJECT_DIR, 'population_images','profiles','%s.jpg'%username)
#         u.picture.save("%s.jpg"%username, File(open(image_path, 'rb')))
#     u.bio = bio
#     # u.email = email
#     u.website = website
#     u.joined = datetime.now()
#     u.save()
#     return user

def add_user(username, password, firstname, surname, bio, email, website):
    # Start with User model first
    user = User.objects.get_or_create(username=username)[0]
    user.password = make_password(password)
    user.email = email
    user.first_name = firstname
    user.last_name = surname
    user.save()
    # Then UserProfile model second
    u = UserProfile.objects.get_or_create(user=user)[0]
    if u.picture.name != "%s.jpg"%username:
        image_path = os.path.join(PROJECT_DIR, 'population_images','profiles','%s.jpg'%username)
        u.picture.save("%s.jpg"%username, File(open(image_path, 'rb')))
    u.bio = bio
    u.website = website
    u.save()
    return user


def add_category(user, name, image_name, views=0):
    c = Category.objects.get_or_create(name=name, user=user)[0]
    image_path = os.path.join(PROJECT_DIR, 'population_images', 'categories', image_name)
    c.picture.save(image_name, File(open(image_path, 'rb')))
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
