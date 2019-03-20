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

    # Load population data from its corresponding csv file
    print("Loading population data...")
    categories = parseCatrgories(os.path.join("population_files","categories.csv"))

    posts = parsePosts(os.path.join("population_files","posts.csv"))

    users = parseUsers(os.path.join("population_files","users.csv"))

    comments = parseComments(os.path.join("population_files","comments.csv"))
    print("Data loaded.")

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
    # 6. Preferences
    # ----------------------------------------------------

    print("Now populating... please wait...")
    print("Adding categories...",end=" ", flush=True)
    for cat in sorted(categories,key=lambda x: x[0]):  # sort the categories by name
        c = add_category(user=superuser, name=cat[0], image_name=cat[1])
    print("DONE")

    print("Adding user profiles and their posts...",end=" ",flush=True)
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
                         post["image"],
                         random.randint(0,100))
    print("DONE")

    print("Adding comments...", end=" ", flush=True)
    # For each post in the database, add 10 random comments from
    # the csv file and assign each comment to a random user
    for post in Post.objects.all():
        # pick how many comments to add to this Post
        how_many = random.randint(5,7)

        # Obtain random samples from users and comments of size "how_many"
        random_users = random.sample(list(User.objects.all()), how_many)
        random_comments = random.sample(comments, how_many)

        # Generate a list of tuples for the two samples --> (user,comment) pairs
        user_comment_pairs = zip(random_users, random_comments)

        for user, comment in user_comment_pairs:
            c = add_comment(user=user, post=post, text=comment)
    print("DONE")

    # Adding random preferences to the 15 most views posts
    print("Adding Preferences...", end=" ", flush=True)
    for post in Post.objects.order_by("-views")[:15]:
        random_users = random.sample(list(User.objects.all()), 5)
        for user in random_users:
            # True -> Liked | False -> Disliked
            p = add_preference(user=user, post=post, liked=bool(random.getrandbits(1)))
    print("DONE")
    print("Finished!")


def create_superuser(username, password):
    superuser = User.objects.get_or_create(username=username)[0]
    superuser.set_password(password)
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.save()
    return superuser


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


def add_post(user, category, title, image_name, views):
    p = Post.objects.get_or_create(title=title, user=user, category=category)[0]
    p.views = views
    image_path = os.path.join(PROJECT_DIR, 'population_images', 'posts', image_name)
    p.image.save(image_name, File(open(image_path, 'rb')))
    p.save()
    return p


def add_comment(user, post, text):
    c = Comment.objects.create(user=user, post=post)
    c.text = text
    c.save()
    return c


def add_preference(user, post, liked):
    p = Preference.objects.get_or_create(user=user, post=post, liked=liked)[0]
    p.save()
    return p





# Start execution here!
if __name__ == '__main__':
    print("Starting Lememe population script...")
    populate()
