from django.contrib import admin
from .models import Category, Breed, Pet

admin.site.register(Category)
admin.site.register(Breed)
admin.site.register(Pet)