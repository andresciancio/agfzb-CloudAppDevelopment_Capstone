from django.contrib import admin
from .models import CarMake,CarModel
# from .models import related models


# Register your models here.

# CarModelInline class
class carModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


# CarModelAdmin class

class CarModelAdmin (admin.ModelAdmin):
    list_display=('name', 'cartype', 'year', 'carmake', 'dealer')
    search_fields=['name', 'year', 'carmake']
    list_filter = ['carmake']

# CarMakeAdmin class with CarModelInline

class CarMakeAdmin(admin.ModelAdmin):
    inlines=[carModelInline]
    list_display=('name', 'description')

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)