from django.test import TestCase
from Corruption_Cove.models import *
from django.urls import reverse

# Create your tests here.
class BankAccountTests(TestCase):
    def test_create_bank_account(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        user_profile = UserProfile.objects.create(user=user, name='testuser')
        user_profile.save()
        bank = Bank.objects.create(username=user_profile, balance=1000, name='testuser', cardNo='1234567812345678', expiry='12/22', cvv='123')
        bank.save()
        self.assertEqual(bank.balance, 1000)
        self.assertEqual(bank.name, 'testuser')
        self.assertEqual(bank.cardNo, '1234567812345678')
        self.assertEqual(bank.expiry, '12/22')
        self.assertEqual(bank.cvv, '123')
        self.assertEqual(bank.slug, 'testuser')

class UserProfileTests(TestCase):
    def test_create_user_profile(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        user_profile = UserProfile.objects.create(user=user, name='testuser')
        user_profile.save()
        self.assertEqual(user_profile.name, 'testuser')
        self.assertEqual(user_profile.user.username, 'testuser')
        self.assertEqual(user_profile.currency, 'GBP')
        self.assertEqual(user_profile.pfp, 'media/images/pfp/default_pfp.png')
        self.assertEqual(user_profile.banner, 'media/images/banner/default_banner.png')
        self.assertEqual(user_profile.blackjack_state, '{}')
        self.assertEqual(user_profile.slug, 'testuser')

class BetTests(TestCase):
    def test_create_bet(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        user_profile = UserProfile.objects.create(user=user, name='testuser')
        user_profile.save()
        bet = Bet.objects.create(username=user_profile, game='blackjack', amount=100)
        bet.save()
        self.assertEqual(bet.username, user_profile)
        self.assertEqual(bet.game, 'blackjack')
        self.assertEqual(bet.amount, 100)
        self.assertEqual(bet.slug, 'testuser')

class RequestTests(TestCase):
    def test_create_request(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        user_profile = UserProfile.objects.create(user=user, name='testuser')
        user_profile.save()
        request = Request.objects.create(sender=user_profile, receiver=user_profile, amount=100)
        request.save()
        self.assertEqual(request.sender, user_profile)
        self.assertEqual(request.receiver, user_profile)
        self.assertEqual(request.amount, 100)
    
class FriendshipTests(TestCase):
    def test_create_friendship(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        user_profile = UserProfile.objects.create(user=user, name='testuser')
        user_profile.save()
        friendship = Friendship.objects.create(sender=user_profile, receiver=user_profile)
        friendship.save()
        self.assertEqual(friendship.sender, user_profile)
        self.assertEqual(friendship.receiver, user_profile)

