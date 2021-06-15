from django.shortcuts import render
from users.models import Member
from django.views.generic.base import TemplateView


class PerfilUptadadeviews(TemplateView):

    template_name = 'socio/perfil.html'


class ConsultationListviews(TemplateView):

    template_name = 'socio/consulta.html'


class MakeDonationviews(TemplateView):

    template_name = 'socio/realizar-doacao.html'


class RequestConsultationviews(TemplateView):

    template_name = 'socio/solicitar-consulta.html'


class ScheduledConsultationsListviews(TemplateView):

    template_name = 'socio/vizualizar-consultas-agendadas.html'


class DonationsMadeListviews(TemplateView):

    template_name = 'socio/vizualizar-doacoes-realizadas.html'
