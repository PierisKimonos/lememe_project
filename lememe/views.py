from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # login_required redirects to index if user is not logged in (see settings.py->)
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Index page works!")

def about(request):
    return HttpResponse("About page works!")

def contact(request):
    return HttpResponse("Contact page works!")
