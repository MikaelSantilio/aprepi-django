from django.contrib.auth import views as auth_views
from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('alterar-senha/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('alterar-senha/feito/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('recuperar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('recuperar-senha/feito/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar/feito/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cadastro/benfeitor/', views.register_benefactor, name="signup-benefactor"),
    path('cadastro/socio/', views.register_member, name="signup-member"),
]
