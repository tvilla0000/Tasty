from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('accounts/signup', views.signup, name='signup'),
    
    path('restaurant/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('restaurant/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    path('restaurant/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    path('restaurant/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurant_delete'),
    
    path('menu/<int:pk>/', views.MenuDetail.as_view(), name="menu_detail"),
    path('menu/<int:pk>/create/', views.MenuCreate.as_view(), name='menu_create'),      
    path('menu/<int:pk>/update', views.MenuUpdate.as_view(), name="menu_update"),
    path('menu/<int:pk>/delete', views.MenuDelete.as_view(), name="menu_delete"),
    
    path('category/<int:pk>/create/', views.CategoryCreate.as_view(), name="category_create"),
    path('category/<int:pk>/update/<int:fk>/', views.CategoryUpdate.as_view(), name="category_update"),
    path('category/<int:pk>/delete/<int:fk>/', views.CategoryDelete.as_view(), name="category_delete"),
    
    path('food/<int:pk>/create/<int:fk>/', views.FoodCreate.as_view(), name='food_create'),          
    path('food/<int:pk>/update/<int:fk>/', views.FoodUpdate.as_view(), name='food_update'),          
]