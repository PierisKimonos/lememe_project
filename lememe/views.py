from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # login_required redirects to index if user is not logged in (see settings.py->)
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.auth.models import User

# Import the models
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the forms
from lememe.forms import UserForm, UserProfileForm, PostForm

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.

    # request.session.set_test_cookie() # inside the about view we check the test_cookie

    # category_list = Category.objects.order_by("-likes")[:5]
    # page_list = Page.objects.order_by("-views")[:5]
    # context_dict = {'categories': category_list, "pages": page_list}
    context_dict = {}
    if request.method == "GET":
        keyword = request.GET.get("keyword",None)
        if keyword:
            context_dict["keyword"] = keyword

        popular_posts = Post.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(popular_posts, 2)
        try:
            popular_posts = paginator.page(page)
        except PageNotAnInteger:
            popular_posts = paginator.page(1)
        except EmptyPage:
            popular_posts = paginator.page(paginator.num_pages)

        context_dict["popular_posts"] = popular_posts

    # Call the helper function to handle the cookies
    # visitor_cookie_handler(request)

    # context_dict['visits'] = request.session.get('visits')

    # Obtain the Response object early so we can add cookie information.
    # this statement can also be before handling cookies in the case of client side cookies
    response = render(request, 'lememe/index.html', context=context_dict)

    # Return response back to user, updating any cookies that need changed.
    return response


def post(request, post_id):
    context_dict = {}
    post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post=post)
    context_dict['post'] = post
    context_dict['comments'] = comments
    return render(request, 'lememe/post.html', context_dict)


def show_category(request, category_name_slug):
    # create a context dictionary which we
    # can pass to the template rendering engine
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated posts.
        # Note that filter() will return a list of post objects or an empty list
        posts = Post.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict["posts"] = posts

        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict["category"] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict["posts"] = None
        context_dict["category"] = None

    # Go render the response and return it to the client.
    return render(request, 'lememe/category.html', context_dict)

def about(request):
    return render(request, 'lememe/about.html', {})

def contact(request):
    return render(request, 'lememe/contact.html', {})

# @login_required
# def upload(request):
#     print("==========>>>>>>>>  here")
#     form = PostForm()
#     print("after postform =================")
#
#     if request.method == 'POST':
#         print("Inside POST ===============")
#         form = PostForm(request.POST)
#         print("++++++++++++++++++++++",form,type(form))
#
#         if form.is_valid():
#             # post = form.save(commit=False)
#             # post.user = request.user
#             # post.views = 0
#             post.save() # client_id is assigned in .save()
#             return post(request, post.id)
#
#         else:
#             print(form.errors)
#
#     print("Above Context Dict ===============")
#     context_dict = {'form': form}
#     return render(request, 'lememe/upload.html', context_dict)

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
            return HttpResponseRedirect(reverse(post, args={"post_id": post.id}))


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
        context_dict = {}

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
                return HttpResponseRedirect(reverse('index'))
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

            return render(request, 'lememe/login.html', context_dict)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'lememe/login.html',
                      {'register_form': False,
                       'user_form': UserForm(),
                       'profile_form': UserProfileForm(),}
                      )


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))
