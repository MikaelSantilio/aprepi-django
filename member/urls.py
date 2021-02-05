from django.urls import path
from member import views

app_name = "member"

urlpatterns = [
    path('perfil/', views.PerfilUptadadeviews.as_view(), name='perfil'),
    path('consultation/', views.ConsultationListviews.as_view(), name='consultation'),  
    path('request-consultation/', views.RequestConsultationviews.as_view(), name='consultation_add'),
    path('consultation-list/', views.ScheduledConsultationsListviews.as_view(), name='consultation_list'),
    path('donation-list/', views.DonationsMadeListviews.as_view(), name='donation_list'),
    path('donation/', views.MakeDonationviews.as_view(), name='donation_add'),
]

