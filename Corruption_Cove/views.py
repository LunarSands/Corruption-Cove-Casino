from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Corruption_Cove.models import UserProfile, Bet
from Corruption_Cove.forms import UserForm, UserProfileForm
from django.http import HttpResponse

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
    try:
        user = UserProfile.objects.get(slug=user_slug)
    except UserProfile.DoesNotExist:
        user = None
    if user is None:
        return redirect('/corruption-cove-casino/')
    
    bets = len(Bet.objects.filter(username=user))
    context = {'topbets' : 0, 'recentbets' : 0}
    if (bets > 0):
        topbets = Bet.objects.get(username=user).order_by('-amount')[:max(3,bets)]
        recentbets = Bet.objects.get(username=user).order_by('-date')[:max(3,bets)]
        context = {'topbets' :  topbets, 'recentbets' : recentbets}

    return render(request, 'Corruption_Cove/account.html',context)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('corruption-cove-casino:index'))

#@login_required
def roulette(request):
    context = {}
    return render(request, "Corruption_Cove/roulette.html", context)