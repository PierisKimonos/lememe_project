from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # login_required redirects to index if user is not logged in (see settings.py->)
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Import the category model
from lememe.models import UserProfile, Post, Comment, Preference, Category
# Import the category form
# from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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

    # Call the helper function to handle the cookies
    # visitor_cookie_handler(request)

    # context_dict['visits'] = request.session.get('visits')

    # Obtain the Response object early so we can add cookie information.
    # this statement can also be before handling cookies in the case of client side cookies
    response = render(request, 'lememe/index.html', context=context_dict)

    # Return response back to user, updating any cookies that need changed.
    return response

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
    return HttpResponse("About page works!")

def contact(request):
    return HttpResponse("Contact page works!")


