from django.contrib import admin
from .models import CarMake, CarModel

# CarModelInline class: Allows CarModel to be edited inline within the CarMake admin page
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of extra empty CarModel forms you want to display

# CarMakeAdmin class: Includes CarModelInline so related CarModels can be edited in CarMake's admin page
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]  # Show CarModelInline within the CarMake admin interface

# CarModelAdmin class: Admin interface for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']  # Fields displayed in the CarModel list view
    list_filter = ['car_make', 'type', 'year']  # Filters for the CarModel list view
    search_fields = ['name']  # Searchable fields

# Register your models here
admin.site.register(CarMake, CarMakeAdmin)  # Register CarMake with its custom admin interface
admin.site.register(CarModel, CarModelAdmin)  # Register CarModel with its custom admin interface
