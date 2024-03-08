from django.urls import path
#from django.conf.urls import url
from Corruption_Cove import views
from Corruption_Cove.games import blackjack


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
path('games/blackjack', views.blackjack, name = 'blackjack'),
path('api/games/blackjack', blackjack.blackjack, name='blackjack_api')
]
