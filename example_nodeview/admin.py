from django.contrib import admin

# Register your models here.
from example_nodeview.models import Person, House


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    model = House
