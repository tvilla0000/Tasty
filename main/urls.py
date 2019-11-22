from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    
    path('restaurant/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('restaurant/create/', views.RestaurantCreate.as_view(), name='restaurant_create'),
    path('restaurant/<int:pk>/update/', views.RestaurantUpdate.as_view(), name='restaurant_update'),
    path('restaurant/<int:pk>/delete/', views.RestaurantDelete.as_view(), name='restaurant_delete'),
    path('restaurant/<int:restaurant_id>/add_restaurant_photo/', views.add_restaurant_photo, name='add_restaurant_photo'),
    
    path('menu/<int:pk>/', views.MenuDetail.as_view(), name="menu_detail"),
    path('menu/<int:pk>/create/', views.MenuCreate.as_view(), name='menu_create'),      
    path('menu/<int:pk>/update', views.MenuUpdate.as_view(), name="menu_update"),
    path('menu/<int:pk>/delete', views.MenuDelete.as_view(), name="menu_delete"),
    path('menu/<int:menu_id>/add_menu_photo/<int:restaurant_id>/', views.add_menu_photo, name='add_menu_photo'),
    path('menu/<int:menu_id>/delete_menu_photo/<int:restaurant_id>/', views.delete_menu_photo, name='delete_menu_photo'),
    
    path('category/<int:pk>/create/', views.CategoryCreate.as_view(), name="category_create"),
    path('category/<int:pk>/update/<int:fk>/', views.CategoryUpdate.as_view(), name="category_update"),
    path('category/<int:pk>/delete/<int:fk>/', views.CategoryDelete.as_view(), name="category_delete"),
    
    path('food/<int:pk>/create/<int:fk>/', views.FoodCreate.as_view(), name='food_create'),          
    path('food/<int:pk>/update/<int:fk>/', views.FoodUpdate.as_view(), name='food_update'),          
    path('food/<int:pk>/delete/<int:fk>/', views.FoodDelete.as_view(), name='food_delete'),      
    path('food/<int:food_id>/add_food_photo/<int:menu_id>/', views.add_food_photo, name='add_food_photo'),
    path('food/<int:food_id>/delete_food_photo/<int:menu_id>/', views.delete_food_photo, name='delete_food_photo'),
    
    path('search/', views.search, name='search'),
]