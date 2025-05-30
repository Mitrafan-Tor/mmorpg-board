from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register, confirm_email
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm/', confirm_email, name='confirm_email'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        form_class=LoginForm
    ), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
   #path('logout/', LogoutView.as_view(), name='logout'),
]