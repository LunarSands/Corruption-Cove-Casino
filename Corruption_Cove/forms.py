from django import forms
from Corruption_Cove.models import UserProfile,Request,Friendship,Bank
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'pfp', 'banner','currency')

class BankForm(forms.ModelForm):
    cardNo = forms.CharField(widget=forms.PasswordInput())
    expiry = forms.DateField(widget=forms.PasswordInput())
    cvv = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Bank
        fields = ('name', 'cardNo', 'expiry', 'cvv', 'balance')
    
    def save(self, signed_in=None):
        bank = super().save(commit=False)
        if signed_in:
            bank.username = signed_in
        bank.save()
        return bank

class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ()

    def save(self, user=None, signed_in=None):
        friendship = super().save(commit=False)
        if user and signed_in:
            friendship.sender = signed_in
            friendship.receiver = user
        friendship.save()
        return friendship

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('amount',)

    def save(self, user=None, signed_in=None):
        request = super().save(commit=False)
        if user and signed_in:
            request.sender = signed_in
            request.receiver = user
        request.save()
        return request