from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from core.views import EmployeeRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, View
from django.views.generic.base import ContextMixin, TemplateResponseMixin
import pdb
from users.forms import (BenefactorSignUpForm, MemberForm, MemberSignUpForm,
                         ProfileRegistrationDataSignUpForm)

User = get_user_model()


# @transaction.atomic
# def register_benefactor(request):
#     if request.method == 'POST':
#         user_form = BenefactorSignUpForm(request.POST)
#         profile_form = ProfileRegistrationDataSignUpForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.save()
#             user.refresh_from_db()
#             profile_form = ProfileRegistrationDataSignUpForm(
#                 request.POST, instance=user.profile)
#             profile_form.full_clean()
#             profile_form.save()
#             messages.success(
#                 request, 'Conta criada com sucesso, faça login para continuar')
#             return HttpResponseRedirect(reverse_lazy('core:home'))
#         else:
#             messages.error(request, 'Erro ao criar sua conta')
#     else:
#         user_form = BenefactorSignUpForm()
#         profile_form = ProfileRegistrationDataSignUpForm()
#     return render(request, 'registration/signup_form.html', {'user_form': user_form, 'profile_form': profile_form})


# @transaction.atomic
# def register_member(request):
#     if request.method == 'POST':
#         user_form = BenefactorSignUpForm(request.POST)
#         profile_form = ProfileRegistrationDataSignUpForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.save()
#             user.refresh_from_db()
#             profile_form = ProfileRegistrationDataSignUpForm(
#                 request.POST, instance=user.profile)
#             profile_form.full_clean()
#             profile_form.save()
#             messages.success(
#                 request, 'Conta criada com sucesso, faça login para continuar')
#             return HttpResponseRedirect(reverse_lazy('core:home'))
#         else:
#             messages.error(request, 'Erro ao criar sua conta')
#     else:
#         user_form = MemberSignUpForm()
#         member_form = MemberForm()
#         profile_form = ProfileRegistrationDataSignUpForm()
#     return render(request, 'registration/signup_form.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'member_form': member_form})


class MemberSignUpView(EmployeeRequiredMixin, TemplateResponseMixin, ContextMixin, View):

    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = MemberSignUpForm()
        member_form = MemberForm()
        profile_form = ProfileRegistrationDataSignUpForm()

        context['user_form'] = user_form
        context['member_form'] = member_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = BenefactorSignUpForm(request.POST)
        profile_form = ProfileRegistrationDataSignUpForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            messages.error(request, 'Erro ao criar sua conta')
            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def form_valid(self, user_form, profile_form):
        user = user_form.save(commit=False)
        user.save()
        user.refresh_from_db()
        profile_form = ProfileRegistrationDataSignUpForm(
            self.request.POST, instance=user.profile)
        profile_form.full_clean()
        profile_form.save()
        messages.success(
            self.request, 'Conta de sócio criada com sucesso')

        return HttpResponseRedirect(reverse_lazy('core:home'))


class BenefactorSignUpView(TemplateResponseMixin, ContextMixin, View):

    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = MemberSignUpForm()
        profile_form = ProfileRegistrationDataSignUpForm()

        context['user_form'] = user_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = BenefactorSignUpForm(request.POST)
        profile_form = ProfileRegistrationDataSignUpForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        else:
            # v = None
            for key, value in profile_form.errors.items():
                for e in value:
                    messages.warning(request, f"{key} - {e}")
            for key, value in user_form.errors.items():
                for e in value:
                    messages.warning(request, f"{key} - {value}")
            # pdb.set_trace()
            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('core:home'))
        return self.render_to_response(self.get_context_data())

    def form_valid(self, user_form, profile_form):
        user = user_form.save(commit=False)
        user.save()
        user.refresh_from_db()
        profile_form = ProfileRegistrationDataSignUpForm(
            self.request.POST, instance=user.profile)
        profile_form.full_clean()
        profile_form.save()
        messages.success(
            self.request, 'Conta criada com sucesso, faça login para continuar')

        return HttpResponseRedirect(reverse_lazy('core:home'))
