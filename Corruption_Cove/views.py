from django.shortcuts import render

def index(request):
    context = {}
    return render(request, "Corruption_Cove/index.html", context)

def nav_bar(request):
    context = {}
    return render(request, "Corruption_Cove/nav.html", context)
