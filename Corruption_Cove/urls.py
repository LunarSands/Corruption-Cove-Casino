from django.urls import path
#from django.conf.urls import url
from Corruption_Cove import views


app_name = 'corruption-cove-casino'

urlpatterns = [
path('', views.index, name='index'),
]
