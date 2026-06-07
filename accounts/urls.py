from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_step1, name="register"),
    path("register/verify/", views.register_step2, name="register_verify"),
    path("register/resend/", views.resend_otp, name="resend_otp"),
    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
    path("profile/", views.profile_view, name="profile"),
]
