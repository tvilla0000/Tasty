from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=200, blank=False)
    address = models.TextField(blank=False)
    phone = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, default='')
    zipcode = models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    restaurant_photo = models.CharField(max_length=300, default='https://s3-us-west-1.amazonaws.com/fishcollector/e5abd9.jpg')    
    
    def __str__(self):
        return f'restaurant name - {self.name}'
    
    def get_absolute_url(self):
        return reverse('restaurant_detail', kwargs={'pk':self.id})

class Menu(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=500, blank=True, default='')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_photo = models.CharField(max_length=300, default='https://s3-us-west-1.amazonaws.com/fishcollector/e5abd9.jpg')
    date = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f'menu name - {self.name}'
    
    def get_absolute_url(self):
        return reverse('menu_detail', kwargs={'pk':self.id})

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
    food_photo = models.CharField(max_length=300, default='https://s3-us-west-1.amazonaws.com/fishcollector/e5abd9.jpg')    
    

    def __str__(self):
        return f'food name - {self.name}'