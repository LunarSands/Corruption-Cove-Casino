from django.shortcuts import render

def index(request):
    context = {}
    return render(request, "Corruption_Cove/index.html", context)