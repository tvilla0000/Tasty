from django.contrib import admin
from .models import Restaurant, Menu, Category, Food, Photo

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Photo)