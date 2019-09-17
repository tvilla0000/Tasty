from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Restaurant, Menu, Category, Food
from .forms import RestaurantForm
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'namecollector'
API_KEY = 'AIzaSyA5PFcm4YZ1KnBSQDyq-Eon2znBNuul95Q&'
MAP_BASE_URL='https://www.google.com/maps/embed/v1/place?key='+API_KEY

def home(request):
    return render(
        request,
        'main/home.html',
    )
    
class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        restaurants = user.restaurant_set.all()
        context['restaurants'] = restaurants
        return context

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            login(request, user)
            return redirect('profile', pk=user.id)
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
    
class RestaurantList(ListView):
    model = Restaurant
    template_name = 'restaurant/restaurant_list.html'
    context_object_name = 'restaurants'
    
class RestaurantDetail(DetailView):
    model = Restaurant
    context_object_name = 'restaurant'
    template_name = 'restaurant/restaurant_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['map'] = MAP_BASE_URL
        return context
    
class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name', 'address', 'phone', 'zipcode', 'description']
    template_name = 'restaurant/restaurant_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        restaurant_form = RestaurantForm()
        context = super().get_context_data(**kwargs)
        context['form'] = restaurant_form
        return context

class RestaurantUpdate(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = ['name', 'address', 'phone', 'zipcode', 'description']
    template_name = 'restaurant/restaurant_form.html'
    
    def get_success_url(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        user = restaurant.user
        return reverse('profile', kwargs={'pk': user.id})
    
class RestaurantDelete(LoginRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurant/restaurant_confirm_delete.html'
    
    def get_success_url(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        user = restaurant.user
        return reverse('profile', kwargs={'pk': user.id})
    
class MenuCreate(LoginRequiredMixin, CreateView):
    model = Menu
    fields = ['name', 'description']
    template_name = 'menu/menu_form.html'

    def form_valid(self, form):
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])        
        form.instance.restaurant = restaurant
        return super().form_valid(form)
    
    def get_success_url(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        return reverse('restaurant_detail', kwargs={'pk': restaurant.id})

class MenuDetail(DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/menu_detail.html'
    
    def get_context_data(self, **kwargs):
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        restaurant = menu.restaurant
        menus = Menu.objects.filter(restaurant_id=restaurant.id)
        context = super().get_context_data(**kwargs)
        context['restaurant'] = restaurant
        context['menus'] = menus
        return context


class MenuUpdate(LoginRequiredMixin, UpdateView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/menu_form.html'
    fields = ['name', 'description']

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        restaurant = menu.restaurant
        return reverse('restaurant_detail', kwargs={'pk': restaurant.id})


class MenuDelete(LoginRequiredMixin, DeleteView):
    model = Menu
    context_object_name = 'menu'
    template_name = "menu/menu_confirm_delete.html"

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        restaurant = menu.restaurant
        return reverse('restaurant_detail', kwargs={'pk': restaurant.id})

    def get_context_data(self, **kwargs):
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        restaurant = menu.restaurant
        context = super().get_context_data(**kwargs)
        context['restaurant'] = restaurant
        return context

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category 
    fields = ['name']
    template_name = 'categories/category_form.html'

    def form_valid(self, form):
        menu = Menu.objects.get(pk=self.kwargs['pk'])        
        form.instance.menu = menu 
        return super().form_valid(form)
    
    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['pk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    context_object_name = 'category'
    template_name = 'categories/category_form.html'
    fields = ['name']

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'categories/category_confirm_delete.html'

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})

    def get_context_data(self, **kwargs):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food 
    fields = ['name', 'price', 'description']
    template_name = 'food/food_form.html'

    def form_valid(self, form):
        category = Category.objects.get(pk=self.kwargs['pk'])        
        form.instance.category = category 
        return super().form_valid(form)
    
    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})
    
class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    context_object_name = 'food'
    template_name = 'food/food_form.html'
    fields = ['name', 'price', 'description']

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})
    
class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    context_object_name = 'food'
    template_name = 'food/food_confirm_delete.html'

    def get_success_url(self):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        return reverse('menu_detail', kwargs={'pk': menu.id})

    def get_context_data(self, **kwargs):
        menu = Menu.objects.get(pk=self.kwargs['fk'])
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
    
def add_menu_photo(request, menu_id, restaurant_id):
    photo_file = request.FILES.get('photo-file', None)
    menu = Menu.objects.get(id=menu_id)    
    restaurant = Restaurant.objects.get(id=restaurant_id)    
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            menu.menu_photo = url
            menu.save()
        except:
            print('An error')
    return redirect(restaurant)

def add_food_photo(request,f_id, menu_id):
    photo_file = request.FILES.get('photo-file', None)
    food = Food.objects.get(id=f_id)
    menu = Menu.objects.get(id=menu_id)    
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            food.food_photo = url
            food.save()
        except:
            print('An error')
    return redirect(menu)

def delete_menu_photo(request, menu_id, restaurant_id):
    menu = Menu.objects.get(id=menu_id)
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menu.menu_photo ='https://s3-us-west-1.amazonaws.com/fishcollector/e5abd9.jpg'
    menu.save()
    return redirect(restaurant)

def delete_food_photo(request, food_id, menu_id):
    menu = Menu.objects.get(id=menu_id)
    food = Food.objects.get(id=food_id)
    food.food_photo ='https://s3-us-west-1.amazonaws.com/fishcollector/e5abd9.jpg'
    food.save()
    return redirect(menu)

def search(request):
    content = request.GET.get('content')
    option = request.GET.get('option')
    error_msg = ''
    if not content:
        error_msg = 'Please type in search content'
        return render(request, 'main/home.html', {'error_msg': error_msg})
    if option == 'name':
        restaurants = Restaurant.objects.filter(name__icontains=content)
    elif option == 'zipcode':
        restaurants = Restaurant.objects.filter(zipcode__exact=content)
    return render(request, 'restaurant/restaurant_list.html', {'error_msg': error_msg,'restaurants': restaurants})