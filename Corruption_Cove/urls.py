from django.urls import path
#from django.conf.urls import url
from Corruption_Cove import views


app_name = 'corruption-cove-casino'

urlpatterns = [
path('', views.index, name='index'),
path('register/', views.register, name='register'),
path('sign-in/', views.signin, name='sign-in'),
path('logout/', views.user_logout, name='logout'),
path('games/', views.games, name='games'),
]
