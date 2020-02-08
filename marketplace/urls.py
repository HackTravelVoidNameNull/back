from django.urls import path
from .views import *

app_name = 'marketplace'
urlpatterns = [
    path('main', MainView.as_view(), name='main')
]