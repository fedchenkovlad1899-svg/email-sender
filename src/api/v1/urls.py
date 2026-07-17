from django.urls import path
from api.v1.users.views import (
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

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profiles/", UserListView.as_view(), name="profiles"),
    path("logout/",LogoutView.as_view(),name="logout",),
    path("change_password/",ChangePasswordView.as_view(),name="change_password",),
    path("users/<int:pk>/",UserDetailView.as_view(),name="user_detail",),
    path("users/<int:pk>/status/",UserStatusView.as_view(),name="user_status",),
    path("users/<int:pk>/delete/",UserDeleteView.as_view(),name="user_delete",),

]