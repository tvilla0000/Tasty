from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .models import Restaurant, Menu



# Create your views here.
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
    
class RestaurantCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name', 'address', 'phone', 'description', 'zipcode']
    template_name = 'restaurant/restaurant_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
    
# class MenuList(ListView):
#     model = Restaurant
#     template_name = 'restaurant/restaurant_list.html'
#     context_object_name = 'restaurants'
    
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

class MenuDetail(LoginRequiredMixin, DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/menu_detail.html'