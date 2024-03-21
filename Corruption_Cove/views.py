from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from Corruption_Cove.decorators import card_required
from Corruption_Cove.games.roulette import ROULETTE_BETS
from Corruption_Cove.forms import *
from django.http import HttpResponse
from random import randint
from django.views import View
from datetime import datetime
import json
import requests
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    context = {}
    users_format={}
    users = User.objects.all()
    for user in users:
        try:
            user.profile
            users_format[user.username] = user.profile.slug
        except ObjectDoesNotExist:
            continue
    context['users'] = json.dumps(users_format)
    print(users_format)
    return render(request, "Corruption_Cove/index.html", context)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'pfp' in request.FILES:
                profile.pfp = request.FILES['pfp']
            if 'banner' in request.FILES:
                profile.banner = request.FILES['banner']
            profile.save()
            registered = True
            login(request,user)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form,'profile_form': profile_form,'registered': registered}
    return render(request,'Corruption_Cove/register.html',context)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('corruption-cove-casino:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Incorrect username or password.")
    else:
        return render(request, 'Corruption_Cove/sign-in.html')

@login_required
def account(request, user_slug):
    context = {}


    #identify who's account page is open
    try:
        user = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        user = None
    if user is None:
        return redirect('/corruption-cove-casino/')

    #check if bank card has been added
    banks = False
    banking = None
    try:
        banking = Bank.objects.get(slug=user_slug)
        banks = True
    except Bank.DoesNotExist:
        banks = False
    context['banking'] = banking
    context['banks'] = banks

    #find top and recent bets from current user
    bets = len(Bet.objects.filter(slug=user_slug))
    context['topbets'] = 0
    context['recentbets'] = 0
    if (bets > 0):
        topbets = Bet.objects.filter(slug=user_slug).order_by('-amount')[:min(3,bets)]
        recentbets = Bet.objects.filter(slug=user_slug).order_by('-date')[:min(3,bets)]
        context['topbets'] =  topbets
        context['recentbets'] = recentbets

    #find friends of current user
    friendsHelper = Friendship.objects.filter(Q(sender=user) | Q(receiver=user))
    friends = []
    for friend in friendsHelper:
        if friend.sender.slug == user.slug:
            friends.append(UserProfile.objects.get(slug=friend.receiver.slug))
        else:
            friends.append(UserProfile.objects.get(slug=friend.sender.slug))
    context['friends'] = friends

    context['friend_exists'] = False
    for friend in friends:
        if (request.user.profile.slug == friend.slug):
            context['friend_exists'] = True


    #find money requests directed at current user
    requests = Request.objects.filter(receiver=user)
    context['requests'] = requests


    #handle form input
    if request.method == 'POST':
        if "submit_f" in request.POST:
            friend_form = FriendshipForm(request.POST)
            if friend_form.is_valid():
                friend_form.save(user=user, signed_in=request.user.profile)
            else:
                print(friend_form.errors)
            context['friend_form'] = friend_form
            return redirect(reverse('corruption-cove-casino:account', args=(user_slug,)))
        if "submit_r" in request.POST:
            request_form = RequestForm(request.POST)
            if request_form.is_valid():
                request_form.save(user=user,signed_in=request.user.profile)
            else:
                print(request_form.errors)
            context['request_form'] = request_form
            return redirect(reverse('corruption-cove-casino:account', args=(user_slug,)))
    else:
        friend_form = FriendshipForm()
        request_form = RequestForm()

    #pass user
    context['account'] = user
    #context['personalRate'] = calculate_personal_rate(request)
    context['personalRate'] = 1

    return render(request, 'Corruption_Cove/account.html',context)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('corruption-cove-casino:index'))



@login_required
def games(request):
    context = {}
    context['slots'] = Slots.objects.all()
    context['dealers'] = Dealer.objects.all()

    return render(request, "Corruption_Cove/games.html", context)

@card_required
@login_required
def roulette(request):
    context = {}

    bets = Bet.objects.filter(game='roulette')
    if (len(bets) > 0):
        context['bets'] = bets.order_by('-amount')[:min(5,len(bets))]

    context['bet_data'] = [{"name":x['name'],"type":x['type']} for x in ROULETTE_BETS]
    #context['personalRate'] = calculate_personal_rate(request)
    context['personalRate'] = 1

    return render(request, "Corruption_Cove/roulette.html", context)

@card_required
@login_required
def blackjack(request,dealer=""):
    context = {}
    add_bets_to_context(context, 'blackjack-' + dealer)
    context['actions'] = {'all':['bet','split','start','clear'],'0':['hit','stay','double_down'],'1':['hit','stay','double_down']}
    try:
        context['dealer'] = Dealer.objects.get(name=dealer)
    except:
        context['dealer'] = None
    #context['personalRate'] = calculate_personal_rate(request)
    context['personalRate'] = 1

    return render(request, "Corruption_Cove/blackjack.html", context)


def add_bets_to_context(context, game):
    bets = Bet.objects.filter(game=game)
    if (len(bets) > 0):
        context['bets'] = bets.order_by('-amount')[:max(5, len(bets))]

@card_required
@login_required
def slots(request,machine):
    context = {}

    add_bets_to_context(context,'slots-'+machine)

    context['machine'] = machine
    
    return render(request, "Corruption_Cove/slots.html", context)

class deposit(View):
    def get(self, request):
        depositValue = float(request.GET["depositValue"])
        userID = request.user.profile.slug
        #personalRate = calculate_personal_rate(request)
        personalRate = 1
        try:
            bank = Bank.objects.get(slug=userID)
        except Bank.DoesNotExist:
            HttpResponse("Bank account not found")

        bank.balance += depositValue/personalRate
        bank.save()
        return HttpResponse(str(bank.balance))


def howToPlay(request,gameType):
    context = {}

    f = open("static\\rules.json", "r")
    rules = json.loads(f.read())
    f.close()

    context['name'] = str(gameType).capitalize()

    context['text'] = rules[str(gameType)]
    
    return render(request, "Corruption_Cove/howToPlay.html", context)

def add_card(request, user_slug):
    context = {}

    if request.method == 'POST':
        bank_form = BankForm(request.POST)

        if bank_form.is_valid():
            bank_form.clean_cardNo()
            bank_form.clean_expiry()
            bank_form.clean_cvv()
            #personalRate = calculate_personal_rate(request)
            personalRate = 1
            bank_form.save(signed_in=UserProfile.objects.get(slug=user_slug), personalRate=personalRate, balance = request.POST.get('balance', None))
            return redirect(reverse('corruption-cove-casino:account', args=(user_slug,)))
        else:
            print(bank_form.errors)
    else:
        bank_form = BankForm()

    context['bank_form'] = bank_form

    return render(request, "Corruption_Cove/add_card.html", context)

def calculate_personal_rate(request):
    # Call API to fetch exchange rates
    endpoint = 'latest'
    access_key = '687d68b03eed20002cc8e226b1756022'
    response = requests.get(f'https://api.exchangeratesapi.io/v1/{endpoint}?access_key={access_key}&symbols=USD,AUD,EUR,JPY,MXN')
    data = response.json()

    #retrieve relevant info to convert from EUR default to user currency
    euro_to_pounds_rate = float(data['rates']['GBP'])
    user_currency_rate = float(data['rates'][request.user.profile.currency])

    # Calculate personal rate
    personal_rate = euro_to_pounds_rate / user_currency_rate

    return personal_rate