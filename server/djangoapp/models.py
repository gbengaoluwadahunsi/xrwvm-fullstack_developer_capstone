# Uncomment the following imports before adding the Model code
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# CarMake Model
class CarMake(models.Model):
    name = models.CharField(max_length=100)  # Name of the car make
    description = models.TextField()  # Description of the car make
    # You can add more fields as needed

    def __str__(self):
        return self.name  # The string representation of CarMake

# CarModel Model
class CarModel(models.Model):
    # Many-to-One relationship to CarMake model (One CarMake can have many CarModels)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)  # Name of the car model

    # Choices for car type
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more options if needed
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')  # Car type

    # Year field with validation
    year = models.IntegerField(
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )

    dealer_id = models.IntegerField()  # Dealer ID, referring to the Cloudant dealer database

    def __str__(self):
        return f'{self.car_make.name} {self.name}'  # String representation includes make and model
