from django.contrib import admin
from .models import Restaurant, Menu, Category, Food

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Food)