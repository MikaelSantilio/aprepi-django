from django.shortcuts import render
from django.views.generic.edit import View
from donations.forms import DonationForm
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin


class MakeDonation(LoginRequiredMixin, View):
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
