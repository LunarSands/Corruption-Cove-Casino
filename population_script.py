import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Corruption_Cove_Casino.settings')

import django
django.setup()
from Corruption_Cove.models import *
import random

random.seed(123)

def populate():
    dealers = {'Babs': {'face':'/media/images/dealers/Babs.png', 'stop':17, 'soft':True}, 
               'Dick': {'face':'/media/images/dealers/Dick.png', 'stop':17, 'soft':False},
               'Jason':{'face':'/media/images/dealers/Jason.png', 'stop':19, 'soft':True},
            }
    slots = {'Egypt': {'preview':'/media/images/slots/Egypt.png'}, 
             'Classic': {'preview':'/media/images/slots/Classic.png'},
             'Fruit':{'preview':'/media/images/slots/Fruit.png'},
            }
    users = [{'name':f'user{x}','pass':f'pass{x}'} for x in range(10)]
    cards = [{'name':f'name{x}','no':random.choices('0123456789',k=16),'expiry':'10/26','cvv':random.choices('0123456789',k=3)} for x in range(10)]

    for user,card in zip(users,cards):
        add_user(user,card)
    
    for dealer,info in dealers.items():
        print(f"Adding dealer: {dealer}")
        add_dealer(dealer, info['face'], info['stop'], info['soft'])

    for machine,info in slots.items():
        print(f"Adding slot machine: {machine}")
        add_machine(machine, info['preview'])

def add_dealer(name, face, stop, soft):
    dealer = Dealer.objects.get_or_create(name=name)[0]
    dealer.stop = stop
    dealer.soft = soft
    dealer.save()

def add_machine(theme, preview):
    machine = Slots.objects.get_or_create(theme=theme)[0]
    machine.preview = preview
    machine.save()

def add_user(user,card):
    user_model = User.objects.get_or_create(username=user['name'])[0]
    user_model.set_password(user['pass'])
    user_prof = UserProfile.objects.get_or_create(user=user_model,name=card['name'])[0]
    card = Bank.objects.get_or_create(username=user_prof,name=card['name'],cvv=card['cvv'],expiry=card['expiry'],cardNo=card['no'],balance=random.randint(0,500))[0]
    user_model.save()
    user_prof.save()
    card.save()


if __name__ == '__main__':
    print('Starting population script...')
    populate()