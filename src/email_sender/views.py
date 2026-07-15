
from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    return render(request, "home.html")

def campaign(request):
    return render(request, "campaign.html")
def contact(request):
    return render(request, "contact.html")
def message_template(request):
    return render(request, "message_template.html")

def statistic(request):
    return render(request, "statistic.html")

def about(request,):

    return render(request, 'about.html')

def index(request):
    return HttpResponse("HELwefwefwefLO")