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
path('account/<slug:user_slug>/',
         views.account, name='account'),
path('games/roulette/', views.roulette, name='roulette'),
path('api/games/blackjack', blackjack.blackjack, name='blackjack_api')
path('games/blackjack/<slug:dealer>/',
         views.blackjack, name='blackjack'),
path('games/slots/<slug:machine>/',
         views.slots, name='slots'),
path('account/<slug:user_slug>/deposit/', views.deposit, name='deposit'),
path('games/roulette/play_roulette/', views.play_roulette.as_view(), name='play_roulette'),
]
