from django.views.generic import TemplateView
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import reverse


class EmployeeRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        elif not request.user.is_employee and not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        elif not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class RequestFormKwargsMixin(object):
    """
    CBV mixin which puts the request into the form kwargs.
    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """
    def get_form_kwargs(self):
        kwargs = super(RequestFormKwargsMixin, self).get_form_kwargs()
        # Update the existing form kwargs dict with the request's user.
        kwargs.update({"request": self.request})
        return kwargs


class HomeView(TemplateView):

    template_name = "core/index.html"

class AboutView(TemplateView):

    template_name = "core/about.html"


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = self.get_cards()
        return context

    def get_cards(self):

        cards = []


        if self.request.user.is_benefactor:
            cards += [
                {
                    "url": reverse("donations:unique-donation"),
                    "title": "Fazer doação",
                    "text": "Faça uma doação para nossa institução"
                },
                {
                    "url": reverse("donations:list"),
                    "title": "Verificar doações feitas",
                    "text": "Verifique o histórico de todas as suas doações feitas."
                },
                {
                    "url": reverse("events:donation"),
                    "title": "Fazer doação para evento",
                    "text": "Faça uma doação paras um dos eventos da nossa instituição."
                },
            ]

        if self.request.user.is_employee or self.request.user.is_superuser:
            cards += [
                {
                    "url": reverse("events:list"),
                    "title": "Listagem de eventos",
                    "text": ""
                },
                {
                    "url": reverse("events:create"),
                    "title": "Criar novo evento",
                    "text": ""
                },
                {
                    "url": reverse("users:signup-member"),
                    "title": "Cadastrar Sócio",
                    "text": ""
                },
                {
                    "url": reverse("users:signup-employee"),
                    "title": "Cadastrar Funcionário",
                    "text": ""
                },
                {
                    "url": reverse("users:signup-voluntary"),
                    "title": "Cadastrar Voluntário",
                    "text": ""
                },
            ]

        return cards
