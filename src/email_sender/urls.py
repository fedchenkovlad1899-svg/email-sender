
from django.urls import path
from email_sender.views import index,about,home,campaign,contact,message_template,statistic



urlpatterns = [
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('home/', home, name='home'),
    path('campaign/', campaign, name='campaign'),
    path('contact/', contact, name='contact'),
    path('message_template/', message_template, name='message_template'),
    path('statistic/', statistic, name='statistic'),

]