from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.TextField(blank=False)
    phone = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, default='')
    zipcode = models.IntegerField(blank=False)

    
    def __str__(self):
        return f'restaurant name - {self.name}'
    
    def get_absolute_url(self):
        return reverse('restaurant_detail', kwargs={'pk':self.id})

class Menu(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=500, blank=True, default='')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'menu name - {self.name}'
    
class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'category name - {self.name}'

class Food(models.Model):
    name = models.CharField(max_length=200, blank=False)
    price = models.FloatField(blank=False)
    description = models.TextField(max_length=500, blank=True, default='')    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'food name - {self.name}'
    
class Photo(models.Model):
    name = models.CharField(max_length=200, blank=False)    
    url = models.CharField(max_length=200)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for food_id: {self.food_id} @{self.url}"

