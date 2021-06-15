from core import views
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('sobre-nos', views.AboutView.as_view(), name='about'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
]
