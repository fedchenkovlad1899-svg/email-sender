
from django.urls import path
from email_sender.views import about,home,campaign,contact,message_template,statistic,login_page,register_page



urlpatterns = [
    path('about/', about, name='about'),
    path('home/', home, name='home'),
    path('campaign/', campaign, name='campaign'),
    path('contact/', contact, name='contact'),
    path('message_template/', message_template, name='message_template'),
    path('statistic/', statistic, name='statistic'),
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),

]