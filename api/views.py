from django.shortcuts import render, redirect
from main.models import Restaurant, Menu, Category, Food
from django.http import JsonResponse

def api(request):
    restaurant = list(Restaurant.objects.values());
    menu = list(Menu.objects.values());
    category = list(Category.objects.values());
    food = list(Food.objects.values());

    data = {
        'restaurant': restaurant,
        'menu': menu,
        'category': category,
        'food': food,
    }
    return JsonResponse(data);
    