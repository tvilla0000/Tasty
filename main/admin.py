from django.contrib import admin
from .models import Restaurant, Menu, Category, Food

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Food)