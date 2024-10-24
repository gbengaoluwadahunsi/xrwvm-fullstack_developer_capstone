from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `get_cars` view to fetch the list of cars
def get_cars(request):
    # Get the count of CarMake objects
    count = CarMake.objects.filter().count()

    # If no car makes exist, populate the data with sample entries
    if count == 0:
        logger.info("No car makes found. Populating with sample data.")
        
        # Create sample CarMake objects
        toyota = CarMake.objects.create(name="Toyota")
        honda = CarMake.objects.create(name="Honda")
        ford = CarMake.objects.create(name="Ford")
        chevrolet = CarMake.objects.create(name="Chevrolet")
        bmw = CarMake.objects.create(name="BMW")
        mercedes = CarMake.objects.create(name="Mercedes-Benz")
        audi = CarMake.objects.create(name="Audi")
        nissan = CarMake.objects.create(name="Nissan")
        hyundai = CarMake.objects.create(name="Hyundai")
        kia = CarMake.objects.create(name="Kia")
        
        # Create sample CarModel objects linked to the above CarMakes
        car_models = [
            CarModel(name="Camry", car_make=toyota),
            CarModel(name="Corolla", car_make=toyota),
            CarModel(name="Civic", car_make=honda),
            CarModel(name="Accord", car_make=honda),
            CarModel(name="Mustang", car_make=ford),
            CarModel(name="Fusion", car_make=ford),
            CarModel(name="Malibu", car_make=chevrolet),
            CarModel(name="Impala", car_make=chevrolet),
            CarModel(name="X5", car_make=bmw),
            CarModel(name="C-Class", car_make=mercedes),
        ]
        
        # Save CarModel objects to the database
        CarModel.objects.bulk_create(car_models)

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

@csrf_exempt
def get_dealerships(request):
    if request.method == "GET":
        state = request.GET.get('state', None)

        dealerships = [
            {"id": 1, "full_name": "Dealer 1", "city": "City 1", "address": "Address 1", "zip": "12345", "state": "State 1"},
            {"id": 2, "full_name": "Dealer 2", "city": "City 2", "address": "Address 2", "zip": "67890", "state": "State 2"},
        ]

        if state and state != "All":
            dealerships = [dealer for dealer in dealerships if dealer['state'] == state]

        return JsonResponse({"status": 200, "dealers": dealerships})
    return JsonResponse({"status": 400, "message": "Bad Request"})
