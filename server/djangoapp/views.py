from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `get_cars` view to fetch the list of cars
def get_cars(request):
    # Get the count of CarMake objects
    count = CarMake.objects.filter().count()
    print(count)
    # If no car makes exist, call the `initiate` function to populate data
    if count == 0:
        # Uncomment the following line if you have the `initiate` function in your code
        # initiate() # Make sure `initiate` is imported if using it here

        logger.info("No car makes found. Initiating data population.")

    # Get all CarModel objects with their related CarMake objects
    car_models = CarModel.objects.select_related('car_make')

    # Build a list of dictionaries with CarModel and CarMake information
    cars = [
        {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        }
        for car_model in car_models
    ]

    # Return the data as a JSON response
    return JsonResponse({"CarModels": cars})

# Other view functions here (login_user, logout_request, registration, etc.)

# Example existing view functions
@csrf_exempt
def login_user(request):
    # Login functionality here
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data["status"] = "Authenticated"
    else:
        data["status"] = "Authentication Failed"
    return JsonResponse(data)

def logout_request(request):
    logout(request)
    data = {"userName": "", "status": "Logged out"}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data.get('userName')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    username_exist = User.objects.filter(username=username).exists()

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})
