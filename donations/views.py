from django.shortcuts import render
from django.views.generic.edit import View
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, DetailView, UpdateView
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


class CreditCardByUserMixin():

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.benefactor.pk != self.request.user.pk:
            raise PermissionDenied()
        else:
            return obj


class ThankYouView(TemplateView):

    template_name = "donations/thankyou.html"


class CreditCardCreateView(LoginRequiredMixin, CreateView):
    template_name = 'donations/credit_card/create.html'
    form_class = CreditCardForm
    success_url = reverse_lazy('donations:list-cc')

    def form_valid(self, form):
        benefactor = get_object_or_404(Benefactor, pk=self.request.user.pk)
        form.instance.benefactor = benefactor
        self.object = form.save()

        return super().form_valid(form)


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
