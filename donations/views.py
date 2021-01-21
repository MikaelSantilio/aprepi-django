from django.shortcuts import render
from django.views.generic.edit import View
from donations.forms import DonationForm, BenefactorForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Benefactor
from django.shortcuts import get_object_or_404


class ActivateBenefactorProfile(View):
    pass


class MakeDonationAuthenticated(LoginRequiredMixin, View):
    template_name = 'donations/make_donation.html'
    form_class = DonationForm
    # success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        context = {}
        if self.request.user:
        exists = Benefactor.objects.filter(user=self.request.user)
        if exists:
            benefactor = get_object_or_404(Benefactor, user=self.request.user)
        else:
            benefactor = Benefactor.objects.create(user=self.request.user)
        # Add in a QuerySet of all the books
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

    def form_invalid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, self.get_context_data())


class MakeDonationUnauthenticated(LoginRequiredMixin, View):
    template_name = 'donations/make_donation.html'
    form_class = DonationForm
    # success_url = '/thanks/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        context = {}
        # Add in a QuerySet of all the books
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

    def form_invalid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)


    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, self.get_context_data())


class MakeRecurringDonation(View):
    pass


class MakeAnonymousDonation(View):
    pass
