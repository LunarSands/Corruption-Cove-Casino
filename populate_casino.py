import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Corruption_Cove_Casino.settings')

import django
django.setup()
from Corruption_Cove.models import *

def populate():
    dealers = {'Babs': {'face':'/media/images/dealers/Babs.png', 'stop':17, 'soft':True}, 
               'Dick': {'face':'/media/images/dealers/Dick.png', 'stop':17, 'soft':False},
               'Jason':{'face':'/media/images/dealers/Jason.png', 'stop':19, 'soft':True},
            }
    
    for dealer,info in dealers.items():
        print(f"Adding dealer: {dealer}")
        add_dealer(dealer, info['face'], info['stop'], info['soft'])

def add_dealer(name, face, stop, soft):
    dealer = Dealer.objects.get_or_create(name=name)[0]
    dealer.stop = stop
    dealer.soft = soft
    dealer.save()

if __name__ == '__main__':
    print('Starting population script...')
    populate()