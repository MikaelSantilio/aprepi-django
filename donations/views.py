from django.shortcuts import render
from django.views.generic.edit import View
from django.views.generic import CreateView, TemplateView
from donations.forms import DonationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import RequestFormKwargsMixin
from django.shortcuts import get_object_or_404
from users.models import Benefactor
from donations.models import Donation, RecurringDonation
from django.contrib import messages
from django.urls import reverse_lazy


class MakeDonation(LoginRequiredMixin, CreateView):
    template_name = 'donations/make_donation.html'
    form_class = DonationForm
    # success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_benefactor'] = self.request.user.is_benefactor
        context['form'] = self.form_class
        return context

    def form_valid(self, form):

        benefactor = get_object_or_404(Benefactor, pk=self.request.user)
        form.instance.benefactor = benefactor

        method = form.instance.method

        form.instance.status = self.get_donation_status(method, benefactor)

        if method == "RCREDIT":
            RecurringDonation.objects.create(benefactor=benefactor, donated_value=form.instance.donated_value)

        form.save()

        return HttpResponseRedirect(reverse_lazy('donations:thankyou'))

    def get_donation_status(self, method, benefactor):
        # Regras de cobrança
        # if method == "CREDIT":
        #     credit_card = benefactor.get_valid_credit_card()

        # elif method == "RCREDIT":
        #     credit_card = benefactor.get_valid_credit_card()

        return "approved"

    def get(self, request, *args, **kwargs):
        if not request.user.is_benefactor:
            messages.add_message(request, messages.WARNING, 'Crie uma conta de benfeitor para doar.')
            return HttpResponseRedirect(reverse_lazy('core:home'))
        return super(MakeDonation, self).get(request, *args, **kwargs)


# class MakeRecurringDonation(View):
#     pass


# class MakeAnonymousDonation(View):
#     pass


class ThankYouView(TemplateView):

    template_name = "donations/thankyou.html"
