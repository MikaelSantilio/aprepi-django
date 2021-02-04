from django.urls import path
from donations import views

app_name = "donations"

urlpatterns = [
    path('', views.MakeDonation.as_view(), name='unique-donation'),
    # path('checkout/<str:value>', views.MPCheckout.as_view(), name='mp-checkout'),
    # path('anonima/', views.MakeAnonymousDonation.as_view(), name='anonymous-donation'),
    # path('recorrente/', views.MakeRecurringDonation.as_view(), name='recurring-donation'),
    path('obrigado/', views.ThankYouView.as_view(), name='thankyou'),
    # path('cartoes/', views.CreditCardListView.as_view(), name='list-cc'),
    # path('cartoes/cadastrar', views.CreditCardCreateView.as_view(), name='create-cc'),
    # path('cartoes/<int:pk>', views.CreditCardDetailView.as_view(), name='detail-cc'),
    # path('cartoes/atualizar/<int:pk>',
    #      views.CreditCardUpdateView.as_view(), name='update-cc'),
    # path('cartoes/apagar/<int:pk>',
    #      views.CreditCardDeleteView.as_view(), name='delete-cc')
]
