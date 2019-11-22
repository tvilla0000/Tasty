from django.shortcuts import render, redirect
from main.models import Restaurant, Menu, Category, Food
from django.http import JsonResponse

def api(request):
    restaurant = list(Restaurant.objects.values());
    menu = list(Menu.objects.values());
    category = list(Category.objects.values());
    food = list(Food.objects.values());
    
    for r in restaurant:
        r['menus'] = []        
        for m in menu:
            m['categories'] = []
            for c in category:
                c['foods'] = []
                for f in food:
                    if f['category_id'] == c['id']:
                        c['foods'].append(f)
                if c['menu_id'] == m['id']:
                    m['categories'].append(c)
            if m['restaurant_id'] == r['id']:
                r['menus'].append(m)
        
    data = {
        'result': restaurant
    }
    return JsonResponse(data);
    