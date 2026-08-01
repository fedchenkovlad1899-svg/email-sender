
from django.shortcuts import render



def home(request):
    return render(request, "home.html")

def about(request,):

    return render(request, 'about.html')

#user
def login_page(request):
    return render(request, "users/login.html")

def register_page(request):
    return render(request, "users/register.html")

def profile_page(request):
    return render(request, "users/profile.html")

def profile_update(request):
    return render(request,"users/profile_update.html")

def change_password_page(request):
    return render(request, "users/change_password_page.html")


#contact
def contact(request):
    return render(request, "contacts/contact.html")

def create_contact_page(request):
    return render(request, "contacts/create_contact_page.html")

def update_contact_page(request, pk):
    return render(request, "contacts/update_contact_page.html",{"contact_id": pk})

def import_contact_page(request):
    return render(request, "contacts/import_contact_page.html")

#contact_group
def contact_group(request):
    return render(request,"contacts/contact_group.html")

def create_contact_group(request):
    return render(request,"contacts/create_contact_group.html")

def update_contact_group(request, pk):
    return render(request,"contacts/update_contact_group.html",{"group_id": pk})




def campaign(request):
    return render(request, "campaigns/campaign.html")

def create_campaign(request):
    return render(request,"campaigns/create_campaign.html")

def update_campaign(request, pk):
    return render(request,"campaigns/update_campaign.html",{"campaign_id": pk})








#message
def message_template(request):
    return render(request, "messages/message_template.html")

def create_message_template(request):
    return render(request, "messages/create_message_template.html")

def update_message_template(request, pk):
    return render(request,"messages/update_message_template.html",{"template_id": pk})



def statistic(request):
    return render(request, "statistic.html")





