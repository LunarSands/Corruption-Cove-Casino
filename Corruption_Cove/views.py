from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Corruption_Cove.models import *
from Corruption_Cove.forms import *
from django.http import HttpResponse
from random import randint
from django.views import View
from datetime import date, datetime
from django.utils.timezone import now

def index(request):
    context = {}
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
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request,'Corruption_Cove/register.html',
                  context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})

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
def games(request):
    return

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
    try:
        banking = Bank.objects.get(slug=user_slug)
        banks = True
    except Bank.DoesNotExist:
        banks = False
    context['banking'] = banking
    context['banks'] = banks


    #find top and recent bets from current user
    bets = len(Bet.objects.filter(slug=user_slug))
    context = {'topbets' : 0, 'recentbets' : 0}
    if (bets > 0):
        topbets = Bet.objects.filter(slug=user_slug).order_by('-amount')[:max(3,bets)]
        recentbets = Bet.objects.filter(slug=user_slug).order_by('-date')[:max(3,bets)]
        context = {'topbets' :  topbets, 'recentbets' : recentbets}

    #find friends of current user
    friendsHelper = Friendship.objects.filter(Q(sender=user) | Q(receiver=user))
    friends = []
    for friend in friendsHelper:
        if friend.sender.slug == user.slug:
            friends.append(UserProfile.objects.get(slug = friend.receiver))
        else:
            friends.append(UserProfile.objects.get(slug = friend.sender))
    context['friends'] = friends


    #find money requests directed at current user
    requests = Request.objects.filter(receiver=user)
    context['requests'] = requests


    #handle form input
    if request.method == 'POST':
        friend_form = FriendshipForm(request.POST)
        request_form = RequestForm(request.POST)
        bank_form = BankForm(request.POST)

        if friend_form.is_valid():
            friend_form.save(user=user, signed_in=request.user.profile)
        if request_form.is_valid():
            request_form.save(user=user,signed_in=request.user.profile)
        if bank_form.is_valid():
            bank_form.save(user=user,signed_in=request.user.profile)
        else:
            print(friend_form.errors, request_form.errors)
    else:
        friend_form = FriendshipForm()
        request_form = RequestForm()
        bank_form = BankForm(request.POST)

    
    #pass forms to page
    context['friend_form'] = friend_form
    context['request_form'] = request_form
    context['bank_form'] = bank_form

    #pass user
    context['account'] = user

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

@login_required
def roulette(request):
    context = {}

    bets = Bet.objects.filter(game='roulette')
    if (len(bets) > 0):    
        context['bets'] = bets.order_by('-amount')[:max(5,bets)]

    return render(request, "Corruption_Cove/roulette.html", context)

@login_required
def blackjack(request,dealer):
    context = {}

    bets = Bet.objects.filter(game='blackjack-'+dealer)
    if (len(bets) > 0):    
        context['bets'] = bets.order_by('-amount')[:max(5,bets)]
    
    return render(request, "Corruption_Cove/blackjack.html", context)

@login_required
def slots(request,machine):
    context = {}
    
    bets = Bet.objects.filter(game='slots-'+machine)
    if (len(bets) > 0):    
        context['bets'] = bets.order_by('-amount')[:max(5,bets)]
    
    return render(request, "Corruption_Cove/slots.html", context)

class deposit(View):
    def get(self, request):
        depositValue = float(request.GET["depostValue"])
        userID = request.user.username
        try:
            bank = Bank.objects.get(username=userID)
        except Bank.DoesNotExist:
            HttpResponse("Bank account not found")
        
        bank.balance += depositValue
        bank.save()
        return HttpResponse(bank.balance)

class play_roulette(View):
    def get(self, currentBets):
        red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        order = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32]
        betTypes = [
            "bet-0", "bet-1", "bet-2", "bet-3", "bet-4", "bet-5", "bet-6", "bet-7", "bet-8", "bet-9", 
            "bet-10", "bet-11", "bet-12", "bet-13", "bet-14", "bet-15", "bet-16", "bet-17", "bet-18", "bet-19", 
            "bet-20", "bet-21", "bet-22", "bet-23", "bet-24", "bet-25", "bet-26", "bet-27", "bet-28", "bet-29", 
            "bet-30", "bet-31", "bet-32", "bet-33", "bet-34", "bet-35", "bet-36", "bet-row1", "bet-row2", "bet-row3", 
            "bet-1st", "bet-2nd", "bet-3rd", "bet-low", "bet-even", "bet-red", "bet-black", "bet-odd", "bet-high"
        ]
        bet = 0
        for bet_type in betTypes:
            bet += int(currentBets.GET.get(bet_type, 0))

        generated = randint(0,36)
        winnings = 0
        result = order[generated]

        if (result != 0):
            if (result % 3 == 0):
                winnings += 3 * int(currentBets.GET.get('bet-row1', 0))
            elif ((result + 1) % 3 == 0):
                winnings += 3 * int(currentBets.GET.get('bet-row2', 0))
            elif ((result + 2) % 3 == 0):
                winnings += 3 * int(currentBets.GET.get('bet-row3', 0))
            if (result < 13 and result > 0):
                winnings += 3 * int(currentBets.GET.get('bet-1st', 0))
            elif (result < 25 and result > 12):
                winnings += 3 * int(currentBets.GET.get('bet-2nd', 0))
            elif (result < 37 and result > 24):
                winnings += 3 * int(currentBets.GET.get('bet-3rd', 0))
            if (result % 2 == 0):
                winnings += 2 * int(currentBets.GET.get('bet-even', 0))
            else:
                winnings += 2 * int(currentBets.GET.get('bet-odd', 0))
            if (result > 0 and result < 19):
                winnings += 2 * int(currentBets.GET.get('bet-low', 0))
            else:
                winnings += 2 * int(currentBets.GET.get('bet-high', 0))
            if (result in red):
                winnings += 2 * int(currentBets.GET.get('bet-red', 0))
            else:
                winnings += 2 * int(currentBets.GET.get('bet-black', 0))
        winnings += 36 * int(currentBets.GET.get('bet-' + str(result), 0))

        num = Bet.objects.all().count()
        newBet = Bet(username=currentBets.user.profile, game='roulette', amount=(winnings-bet), date=datetime.now())
        newBet.save()

        return HttpResponse(str(generated) + ':' +str(winnings))

class add_friend(View):
    def get(self):
        friendship = Friendship