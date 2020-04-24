from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'auth'
urlpatterns = [
    path('', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='authentication/password-reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication/password-reset-done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication/password-reset-confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password-reset-complete.html'),
         name='password_reset_complete'),
]
