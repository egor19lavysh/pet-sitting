from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
 
from users.models import User, Petsitter, Region, City
admin.site.register(User, UserAdmin)
admin.site.register(Petsitter) 
admin.site.register(Region) 
admin.site.register(City) 