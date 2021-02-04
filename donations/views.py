from django.shortcuts import render
from core import mercadopago
from django.conf import settings

from django.views.generic.base import ContextMixin
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, DetailView, UpdateView, View
from donations.forms import DonationForm, CreditCardForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from core.views import RequestFormKwargsMixin
from django.shortcuts import get_object_or_404
from users.models import Benefactor
from donations.models import Donation, RecurringDonation
from django.contrib import messages
from donations.models import CreditCard
from events.models import EventDonation
from django.urls import reverse_lazy


class MakeDonation(LoginRequiredMixin, CreateView):
    template_name = 'donations/make_donation.html'
    form_class = DonationForm
    # success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_benefactor'] = self.request.user.is_benefactor
        context['form'] = self.form_class
        context['form_title'] = "FAZER DOAÇÃO"
        return context

    def form_valid(self, form):

        benefactor = get_object_or_404(Benefactor, pk=self.request.user)
        form.instance.benefactor = benefactor

        method = "CREDIT"
        form.instance.method = method
        donated_value = form.instance.donated_value

        form.instance.status = "approved"

        if method == "RCREDIT":
            RecurringDonation.objects.create(benefactor=benefactor, donated_value=form.instance.donated_value)

        form.save()

        init_point = self.get_preference_id(donated_value, "Doação APREPI")

        return HttpResponseRedirect(init_point)

    def get(self, request, *args, **kwargs):
        if not request.user.is_benefactor:
            messages.add_message(request, messages.WARNING, 'Crie uma conta de benfeitor para doar.')
            return HttpResponseRedirect(reverse_lazy('core:home'))
        return super(MakeDonation, self).get(request, *args, **kwargs)

    def get_preference_id(self, value, title):

        mp = mercadopago.MP(settings.TOKEN_MERCADO_PAGO)

        preference = {
            "items": [
                {
                    "title": title,
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(value)
                }
            ],
            "back_urls": {
                "success": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou"))),
                "pending": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou"))),
                "failure": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou")))
            }
        }

        obj = mp.create_preference(preference)

        obj = mp.create_preference(preference)
        return obj['response']['init_point']


class MPCheckout(LoginRequiredMixin, TemplateView):
    template_name = 'donations/mp_checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preference_id'] = self.get_preference_id(self.kwargs.get('value'))[0]
        context['init_point'] = self.get_preference_id(self.kwargs.get('value'))[1]
        return context

    def get(self, request, value, *args, **kwargs):
        if not self.check_float(value):
            messages.add_message(request, messages.WARNING, 'Um erro ocorreu. Tente novamente mais tarde.')
            return HttpResponseRedirect(reverse_lazy('core:dashboard'))
        return super().get(request, *args, **kwargs)

    def check_float(self, potential_float):
        try:
            float(potential_float)

            return True
        except ValueError:
            return False

    def get_preference_id(self, value):
        if not self.check_float(value):
            return None

        mp = mercadopago.MP(settings.TOKEN_MERCADO_PAGO)

        preference = {
            "items": [
                {
                    "title": "Doacao",
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": float(value)
                }
            ],
            "back_urls": {
                "success": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou"))),
                "pending": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou"))),
                "failure": str(self.request.build_absolute_uri(reverse_lazy("donations:thankyou")))
            }
        }

        obj = mp.create_preference(preference)

        obj = mp.create_preference(preference)
        return [obj['response']['id'], obj['response']['init_point']] 


class CreditCardByUserMixin():

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.benefactor.pk != self.request.user.pk:
            raise PermissionDenied()
        else:
            return obj


class ThankYouView(TemplateView):

    template_name = "donations/thankyou.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.GET.get('status'))
        context['status'] = self.request.GET.get('status')
        return context


class CreditCardCreateView(LoginRequiredMixin, CreateView):
    template_name = 'donations/credit_card/create.html'
    form_class = CreditCardForm
    success_url = reverse_lazy('donations:list-cc')

    def form_valid(self, form):
        benefactor = get_object_or_404(Benefactor, pk=self.request.user.pk)
        form.instance.benefactor = benefactor
        self.object = form.save()

        return super().form_valid(form)


class DonationListView(LoginRequiredMixin, ListView):

    model = Donation
    template_name = 'donations/list.html'

    def get_queryset(self):
        return Donation.objects.filter(benefactor__pk=self.request.user.pk).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_donation_list'] = EventDonation.objects.filter(benefactor__pk=self.request.user.pk).order_by('-created_at')
        return context


class CreditCardListView(LoginRequiredMixin, ListView):

    model = CreditCard
    template_name = 'donations/credit_card/list.html'

    def get_queryset(self):
        return CreditCard.objects.filter(benefactor__pk=self.request.user.pk)


class CreditCardDetailView(LoginRequiredMixin, CreditCardByUserMixin, DetailView):

    model = CreditCard
    template_name = 'donations/credit_card/detail.html'
    context_object_name = 'credit_card'


class CreditCardUpdateView(LoginRequiredMixin, CreditCardByUserMixin, UpdateView):

    model = CreditCardByUserMixin
    template_name = 'donations/credit_card/update.html'
    form = CreditCardForm
    context_object_name = 'credit_card'

    def get_success_url(self):
        return reverse_lazy('donations:detail-cc', kwargs={'pk': self.object.id})


class CreditCardDeleteView(LoginRequiredMixin, CreditCardByUserMixin, DeleteView):

    model = CreditCard
    template_name = 'donations/credit_card/delete.html'
    success_url = reverse_lazy('donations:list-cc')
