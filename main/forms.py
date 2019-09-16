from django.forms import ModelForm
from .models import Restaurant

class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'zipcode', 'phone', 'description']
        
        help_texts = {
            'name': ('Name of your restaurant'),
            'address': ('Please type in a correct address for your restaurant, eg: 225 Bush St, San Francisco, CA.'),
            'zipcode': ('Please type in your 5 digit zip code.'),            
            'phone': ('eg: 415-123-4567.'),
        }
        