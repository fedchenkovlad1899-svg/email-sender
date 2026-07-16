from django.urls import path
from api.v1.users.views import RegisterView,LoginView,ProfileView,UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profiles/", UserListView.as_view(), name="profiles"),

]