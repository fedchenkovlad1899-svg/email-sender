
from django.shortcuts import render



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

def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")
