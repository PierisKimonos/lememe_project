from datetime import datetime
import random, json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required # login_required redirects to index if user is not logged in (see settings.py->)
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.templatetags.staticfiles import static


# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm, CommentForm,\
    UpdateUserSettingsForm, UpdateUserProfileSettingsForm, PasswordChangeCustomForm

def index(request):
    context_dict = {}
    if request.method == "GET":
        keyword = request.GET.get("keyword",None)
        if keyword:
            context_dict["keyword"] = keyword

        # Popular posts paging
        popular_posts = Post.objects.all().order_by("-views")
        popular_page = request.GET.get('popular_page', 1)

        popular_paginator = Paginator(popular_posts, 2)
        try:
            popular_posts = popular_paginator.page(popular_page)
        except PageNotAnInteger:
            popular_posts = popular_paginator.page(1)
        except EmptyPage:
            popular_posts = popular_paginator.page(popular_paginator.num_pages)

        context_dict["popular_posts"] = popular_posts

        # New posts paging
        new_posts = Post.objects.all().order_by("-date")
        new_page = request.GET.get('new_page', 1)

        if request.GET.get('new_page') != None:
            context_dict["activate_new_tab"] = True
        else:
            context_dict["activate_new_tab"] = False

        new_paginator = Paginator(new_posts, 2)
        try:
            new_posts = new_paginator.page(new_page)
        except PageNotAnInteger:
            new_posts = new_paginator.page(1)
        except EmptyPage:
            new_posts = new_paginator.page(new_paginator.num_pages)

        context_dict["new_posts"] = new_posts

    # Call the helper function to handle the cookies
    # visitor_cookie_handler(request)

    # context_dict['visits'] = request.session.get('visits')

    # Obtain the Response object early so we can add cookie information.
    # this statement can also be before handling cookies in the case of client side cookies
    response = render(request, 'lememe/index.html', context=context_dict)

    # Return response back to user, updating any cookies that need changed.
    return response


@login_required
def comment(request,post):
    # create a form instance and populate it with data from the request:
    form = CommentForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        # redirect to a new URL:
        # return HttpResponseRedirect(reverse('lememe:show_post', args=[request.post.id]))
    else:
        form = CommentForm()

@csrf_exempt
def ajax_create_comment(request,post_id):
    print("in ajax view")
    # try:
    post = Post.objects.get(client_id=post_id)
    # except Post.DoesNotExist:
    #     post = None

    print("got the post")
    if request.method == 'POST' and post is not None:
        comment_text = request.POST.get('comment_text')
        response_data = {}

        comment = Comment.objects.create(text=comment_text, user=request.user, post=post)
        comment.save()

        response_data['result'] = 'Create post successful!'
        response_data['commentpk'] = comment.pk
        response_data['text'] = comment.text
        response_data['created'] = comment.date.strftime('%b. %d, %Y, %I:%M %p')
        response_data['user'] = comment.user.username
        response_data['number_of_comments'] = int(Comment.objects.filter(post=post).count())
        response_data['post'] = post.client_id

        print("got here")
        try:
            # if user doesn't have a profile picture send the default pic url
            user_profile = UserProfile.objects.get(user=comment.user)
            response_data['user_pic_url'] = user_profile.picture.url
        except UserProfile.DoesNotExist:
            response_data['user_pic_url'] = static('images/placeholder_profile.png')


        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@csrf_exempt
def ajax_add_preference(request,post_id):

    try:
        post = Post.objects.get(client_id=post_id)
    except Post.DoesNotExist:
        return None

    if request.method == 'POST' and post is not None:
        preference = request.POST.get('preference')
        print(preference)

        if preference == "true":
            preference = True
        else:
            preference = False

        response_data = {}

        # Check if a preference already exists in the database
        try:
            old_preference = Preference.objects.get(user=request.user, post=post)
        except Preference.DoesNotExist:
            old_preference = None

        # If the user post preference exists, update the liked attribute
        if old_preference:
            old_preference.liked = preference
            old_preference.save()
        else:
            # If it does not exist, create it
            new_preference = Preference.objects.create(user=request.user, post=post, liked=preference)
            new_preference.save()

        # Likes Ratio
        response_data['like_ratio'] = post.get_rating()
        # What user's preference is
        response_data['preference'] = preference

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def show_post(request, post_id):
    context_dict = {}

    try:
        # Check if a post with the given client id exists
        post = Post.objects.get(client_id=post_id)

        # increment the post's view count
        # post.views += 1
        # post.save()
        post.increament_view_count()

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            comment(request, post)

        comments = Comment.objects.filter(post=post).order_by('-date')
        context_dict['post'] = post
        context_dict['comments'] = comments
        context_dict['comment_form'] = CommentForm()

        return render(request, 'lememe/post.html', context_dict)

    except Post.DoesNotExist:
        # If the requested post does not exist redirect to homepage
        return HttpResponseRedirect(reverse('lememe:index'))






def show_category(request, category_name_slug):

    context_dict = {}

    if request.method == "GET":

        try:
            # Can we find a category name slug with the given name?
            # If we can't, the .get() method raises a DoesNotExist exception.
            # So the .get() method returns one model instance or raises an exception.
            category = Category.objects.get(slug=category_name_slug)


            # Popular posts paging
            # Filter by Category
            popular_posts = Post.objects.filter(category=category).order_by("-views")
            popular_page = request.GET.get('popular_page', 1)

            popular_paginator = Paginator(popular_posts, 2)
            try:
                popular_posts = popular_paginator.page(popular_page)
            except PageNotAnInteger:
                popular_posts = popular_paginator.page(1)
            except EmptyPage:
                popular_posts = popular_paginator.page(popular_paginator.num_pages)

            context_dict["popular_posts"] = popular_posts

            # New posts paging
            # Filter by Category
            new_posts = Post.objects.filter(category=category).order_by("-date")
            new_page = request.GET.get('new_page', 1)

            if request.GET.get('new_page') != None:
                context_dict["activate_new_tab"] = True
            else:
                context_dict["activate_new_tab"] = False

            new_paginator = Paginator(new_posts, 2)
            try:
                new_posts = new_paginator.page(new_page)
            except PageNotAnInteger:
                new_posts = new_paginator.page(1)
            except EmptyPage:
                new_posts = new_paginator.page(new_paginator.num_pages)

            context_dict["new_posts"] = new_posts
            context_dict['active_cat'] = category

        except Category.DoesNotExist:
            # if Category does not exist, return None in context dictionary
            return HttpResponseRedirect(reverse('lememe:index'))

    # Go render the response and return it to the client.
    return render(request, 'lememe/category.html', context=context_dict)


def about(request):

    return render(request, 'lememe/about.html', {})

def contact(request):
    return render(request, 'lememe/contact.html', {})


def show_profile(request, username):
    context_dict = {}
    # In case no user with this username exists
    try:
        user = User.objects.get(username=username)
        profile = UserProfile.objects.get(user=user)
        posts = Post.objects.filter(user=user)
        liked_posts = Preference.objects.filter(user=user)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        # If the user profile does not exist, redirect to homepage
        return HttpResponseRedirect(reverse('lememe:index'))

    context_dict['display_user'] = user
    context_dict['profile'] = profile
    context_dict['posts'] = posts
    context_dict['liked_posts'] = liked_posts
    return render(request, 'lememe/profile.html', context_dict)

@login_required
def show_settings(request):
    context_dict = {}
    # In the settings page we have two forms
    # One is settings_form
    # Other is password_form
    profile = UserProfile.objects.get(user=request.user)

    # Deal with settings form
    if 'settings_form' in request.POST and request.method == 'POST':
        user_form = UpdateUserSettingsForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileSettingsForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)

            # We also need to store the uploaded profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            return HttpResponseRedirect(reverse('lememe:show_profile',args=[request.user.username]))
    else:
        user_form = UpdateUserSettingsForm(instance=request.user)
        profile_form = UpdateUserProfileSettingsForm(instance=profile)

    # Deal with password form
    if 'password_form' in request.POST and request.method == 'POST':
        change_password_form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        # cleaned_data = change_password_form.clean()
        # print(cleaned_data)

        # print('password form is', change_password_form.is_valid())
        if change_password_form.is_valid():
            change_password_form.save()
            update_session_auth_hash(request, change_password_form.user)
            # If the password is changed successfully, redirect to user's profile page
            return HttpResponseRedirect(reverse('lememe:show_profile', args=[request.user.username]))
        else:
            pass
    else:
        change_password_form = PasswordChangeCustomForm(user=request.user)

    # load forms in context dictionary
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['change_password_form'] = change_password_form

    return render(request, 'lememe/settings.html', context_dict)

def feeling_lucky(request):
    # pick a post at random and display it
    random_post = random.choice(Post.objects.all())
    return HttpResponseRedirect(reverse('lememe:show_post', args=[random_post.client_id]))


def search(request):
    context_dict = {}
    if request.method == "GET":
        keyword = request.GET.get("keyword",None)
        if keyword:
            context_dict["keyword"] = keyword

        # Obtain results
        results = Post.objects.filter(title__contains=keyword).order_by("-date")
        # popular_page = request.GET.get('popular_page', 1)
        #
        # popular_paginator = Paginator(popular_posts, 2)
        # try:
        #     popular_posts = popular_paginator.page(popular_page)
        # except PageNotAnInteger:
        #     popular_posts = popular_paginator.page(1)
        # except EmptyPage:
        #     popular_posts = popular_paginator.page(popular_paginator.num_pages)
        #
        # context_dict["popular_posts"] = popular_posts


        context_dict["results"] = results

    # Call the helper function to handle the cookies
    # visitor_cookie_handler(request)

    # context_dict['visits'] = request.session.get('visits')

    # Obtain the Response object early so we can add cookie information.
    # this statement can also be before handling cookies in the case of client side cookies
    response = render(request, 'lememe/search.html', context=context_dict)

    # Return response back to user, updating any cookies that need changed.
    return response

@login_required
def upload(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            post = form.save(commit=False)
            post.user = request.user

            # We also need to store the uploaded image file
            if 'image' in request.FILES:
                post.image = request.FILES['image']
            post.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('lememe:show_post', args=[post.client_id]))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'lememe/upload.html', {'form': form})


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True

            # Once registration is complete, redirect to login page
            return HttpResponseRedirect(reverse('lememe:login'))
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'lememe/login.html',
           {'register_form': True,
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered}
           )


def user_login(request):
    context_dict = {}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.

                # if remember me option is unchecked, expire session immediately
                if not request.POST.get('remember_me'):
                    request.session.set_expiry(0)

                login(request, user)
                return HttpResponseRedirect(reverse('lememe:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Lememe account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.

            # Check what error we have
            if User.objects.filter(username=username).count() == 0: # no record with this username
                context_dict['login_error'] = "No user with this username \"%s\" exists"%username
            else:
                context_dict['login_error'] = "The combination does not match"

    # The boolean register_form is used for the template to know which tab
    # to have activated on the login page. Login or Register?
    context_dict['register_form'] = False
    context_dict['user_form'] = UserForm()
    context_dict['profile_form'] = UserProfileForm()

    return render(request, 'lememe/login.html',context_dict)


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('lememe:index'))
