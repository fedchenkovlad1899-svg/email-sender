
from django.urls import path
from email_sender.views import (
    about,
    home,
    campaign,
    create_campaign,
    update_campaign,
    contact,
    create_contact_page,
    update_contact_page,
    import_contact_page,
    contact_group,
    create_contact_group,
    update_contact_group,
    message_template,
    create_message_template,
    update_message_template,
    statistic,
    login_page,
    register_page,
    profile_page,
    profile_update,
    change_password_page
)



urlpatterns = [
    path('about/', about, name='about'),
    path('home/', home, name='home'),
    #campaign
    path('campaign/', campaign, name='campaign'),
    path('campaign/create', create_campaign, name='create_campaign'),
    path('campaign/<int:pk>/update', update_campaign, name='update_campaign'),
    #contact
    path('contact/', contact, name='contact'),
    path('contact/create', create_contact_page, name='create_contact_page'),
    path('contact/<int:pk>/update', update_contact_page, name='update_contact_page'),
    path('contact/import', import_contact_page, name='import_contact_page'),
    #contact_group
    path('contact/group', contact_group, name='contact_group'),
    path('contact/group/create', create_contact_group, name='create_contact_group'),
    path("contact/group/<int:pk>/update",update_contact_group,name="update_contact_group"),
    #message
    path('message_template/', message_template, name='message_template'),
    path('message_template/create', create_message_template,name="create_message_template"),
    path('message_template/<int:pk>/update', update_message_template,name="update_message_template"),


    path('statistic/', statistic, name='statistic'),
    #user
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("profile/", profile_page, name="profile_page"),
    path("profile/update/", profile_update, name="profile_update"),
    path("profile/change_password/",change_password_page,name="change_password_page",
),


]