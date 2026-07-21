from django.urls import path
from api.v1.views.users import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    LogoutView,
    ChangePasswordView,
    UserDetailView,
    UserStatusView,
    UserDeleteView
)
from api.v1.views.contacts import (
    ContactListView,
    ContactCreateView,
    ContactRetrieveView,
    ContactUpdateView,
    ContactDeleteView,
)
from api.v1.views.message_templates import (
    MessageTemplateListView,
    MessageTemplateCreateView,
    MessageTemplateRetrieveView,
    MessageTemplateUpdateView,
    MessageTemplateDeleteView
)
from api.v1.views.contact_groups import (
    ContactGroupListView,
    ContactGroupCreateView,
    ContactGroupRetrieveView,
    ContactGroupUpdateView,
    ContactGroupDeleteView
)

from api.v1.views.campaigns import (
    CampaignListView,
    CampaignCreateView,
    CampaignRetrieveView,
    CampaignUpdateView,
    CampaignDeleteView
)



urlpatterns = [
    #users
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profiles/", UserListView.as_view(), name="profiles"),
    path("logout/",LogoutView.as_view(),name="logout",),
    path("change_password/",ChangePasswordView.as_view(),name="change_password",),
    path("users/<int:pk>/",UserDetailView.as_view(),name="user_detail",),
    path("users/<int:pk>/status/",UserStatusView.as_view(),name="user_status",),
    path("users/<int:pk>/delete/",UserDeleteView.as_view(),name="user_delete",),
    #contacts
    path("contacts/list",ContactListView.as_view(),name="contact_list",),
    path("contacts/create/",ContactCreateView.as_view(),name="contact_create",),
    path("contacts/<int:pk>/", ContactRetrieveView.as_view(),name="contact_detail",),
    path("contacts/<int:pk>/update/",ContactUpdateView.as_view(),name="contact_update",),
    path("contacts/<int:pk>/delete/",ContactDeleteView.as_view(),name="contact_delete",),
    #message_templates
    path("messages/",MessageTemplateListView.as_view(),name="message_list",),
    path("messages/create/",MessageTemplateCreateView.as_view(),name="message_create",),
    path("messages/<int:pk>/",MessageTemplateRetrieveView.as_view(), name="template_detail",),
    path("messages/<int:pk>/update/",MessageTemplateUpdateView.as_view(),name="template_update",),
    path("messages/<int:pk>/delete/",MessageTemplateDeleteView.as_view(),name="template_delete",),
    #contact_groups
    path("groups/",ContactGroupListView.as_view(),name="contact_group_list",),
    path("groups/create/",ContactGroupCreateView.as_view(),name="contact_group_create",),
    path("groups/<int:pk>/",ContactGroupRetrieveView.as_view(),name="contact_group_detail",),
    path("groups/<int:pk>/update/",ContactGroupUpdateView.as_view(),name="contact_group_update",),
    path("groups/<int:pk>/delete/",ContactGroupDeleteView.as_view(),name="contact_group_delete",),
    #campaigns
    path("campaigns/",CampaignListView.as_view(),name="campaign_list",),
    path("campaigns/create/",CampaignCreateView.as_view(),name="campaign_create",),
    path("campaigns/<int:pk>/",CampaignRetrieveView.as_view(),name="campaign_detail",),
    path("campaigns/<int:pk>/update/",CampaignUpdateView.as_view(),name="campaign_update",),
    path("campaigns/<int:pk>/delete/",CampaignDeleteView.as_view(),name="campaign_delete",),


]



