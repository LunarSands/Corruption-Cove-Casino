from django.urls import path
#from django.conf.urls import url
from Corruption_Cove import views
from Corruption_Cove.games import blackjack
from Corruption_Cove.games import roulette
from Corruption_Cove.games import slots
from Corruption_Cove.games import slots

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
path('api/games/blackjack/<slug:dealer>/', blackjack.blackjack, name='blackjack_api'),
path('api/games/blackjack/<slug:dealer>/', blackjack.blackjack, name='blackjack_api'),
path('games/blackjack/<slug:dealer>/',
         views.blackjack, name='blackjack'),
path('games/blackjack/',views.blackjack),
path('games/blackjack/',views.blackjack),
path('games/slots/<slug:machine>/',
         views.slots, name='slots'),
path('api/games/slots/', slots.slots, name='slots_api'),
path('api/games/slots/', slots.slots, name='slots_api'),
path('deposit/', views.deposit.as_view(), name='deposit'),
path('games/roulette/play_roulette/',roulette.play_roulette , name='play_roulette'),
path('games/roulette/play_roulette/',roulette.play_roulette , name='play_roulette'),
path('account/<slug:user_slug>/add_card/', views.add_card, name='add_card'),
path('request_money/', views.money_request.as_view(), name='request_money'),
path('friend_request/', views.friend_request.as_view(), name='friend_request'),
path('howToPlay/<slug:gameType>/', views.howToPlay, name='howToPlay'),
path('howToPlay/<slug:gameType>/', views.howToPlay, name='howToPlay'),
path('request_accept/', views.request_accept.as_view(), name='request_accept'),
path('request_decline/', views.request_decline.as_view(), name='request_decline'),
path('account/<slug:user_slug>/change_card/', views.change_card, name='change_card'),
]
