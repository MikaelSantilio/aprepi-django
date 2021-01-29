from django.shortcuts import render
from django.views.generic.edit import View
from donations.forms import DonationForm
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import RequestFormKwargsMixin


class MakeDonation(LoginRequiredMixin, RequestFormKwargsMixin, View):
    template_name = 'donations/make_donation.html'
    form_class = DonationForm
    # success_url = '/thanks/'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(AddMeal, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        context = {}
        # Add in a QuerySet of all the books
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        benefactor = self.request.user.benefactor
        form.instance.benefactor = benefactor

        print('\n\n\n########')
        print(form.instance)
        print('\n\n\n########')


        # self.validate_donation(form.instance.method, benefactor)    

        # return super().form_valid(form)

    # def form_invalid(self, form):
    #     return super().form_valid(form)
    

    def validate_donation(self, method, benefactor):

        if form.instance.method == "CREDIT":
            # Lanca excecao se nao tiver
            benefactor.get_valid_credit_card()
            # aqui acontece a logica de cobranca


    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.template_name, self.get_context_data())


class MakeRecurringDonation(View):
    pass


class MakeAnonymousDonation(View):
    pass
