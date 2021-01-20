from django.urls import path
from donations import views

urlpatterns = [
    path('unica/', views.MakeDonation.as_view(), name='unique-donation'),
    path('anonima/', views.MakeAnonymousDonation.as_view(), name='anonymous-donation'),
    path('recorrente/', views.MakeRecurringDonation.as_view(), name='recurring-donation'),
]
