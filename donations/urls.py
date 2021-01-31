from django.urls import path
from donations import views

app_name = "donations"

urlpatterns = [
    path('', views.MakeDonation.as_view(), name='unique-donation'),
    # path('anonima/', views.MakeAnonymousDonation.as_view(), name='anonymous-donation'),
    # path('recorrente/', views.MakeRecurringDonation.as_view(), name='recurring-donation'),
    path('obrigado/', views.ThankYouView.as_view(), name='thankyou'),
]
