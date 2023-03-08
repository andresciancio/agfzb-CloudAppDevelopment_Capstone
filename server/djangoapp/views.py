from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from .models import CarModel
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            context['message'] = "Error: Invalid username or password"
            return render(request, 'djangoapp/index.html', context)
    else:
        context['message'] = "Error: Invalid username or password"
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user already exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error('New user')
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, 
                                            password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/50c44206-3274-4b15-a89b-5e6f5b8c9bf2/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = dict()
        context["dealership"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == 'GET':
        context = dict()
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/50c44206-3274-4b15-a89b-5e6f5b8c9bf2/dealership-package/get-dealership"
        dealership = get_dealers_from_cf(url, id=dealer_id)
        url="https://us-south.functions.appdomain.cloud/api/v1/web/50c44206-3274-4b15-a89b-5e6f5b8c9bf2/dealership-package/get-reviews"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        context['reviews'] = reviews
        context['dealership'] = dealership


        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = dict()
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/50c44206-3274-4b15-a89b-5e6f5b8c9bf2/dealership-package/get-dealership"
    dealership = get_dealers_from_cf(url, id=dealer_id)

    context['dealership'] = dealership
    context['dealer_id'] = dealer_id
    context['cars'] = CarModel.objects.all()

    if request.method == 'GET':
         return render(request, 'djangoapp/add_review.html', context)

    if request.method == 'POST':
      if request.user.is_authenticated:
            car = CarModel.objects.get(pk=request.POST['car'])
        
            
            review = dict()   
            review["time"] = datetime.utcnow().isoformat()
            review["purchase"] = request.POST['purchasecheck']
            review["purchase_date"] = request.POST['purchasedate']
            review["dealership"] = dealer_id
            review["name"] = "andy andy"
            review["car_make"] = car.carmake.name
            review["car_model"] =  car.name
            review["car_year"] = '2023'
            review["review"] = request.POST['content']
            json_payload = dict()
            json_payload["review"] = review
            url ="https://us-south.functions.appdomain.cloud/api/v1/web/50c44206-3274-4b15-a89b-5e6f5b8c9bf2/dealership-package/post-review"
            print (json_payload)
            post_request(url, json_payload)
            return render(request, 'djangoapp/dealer_details.html', context)
        
   
            
# ...

