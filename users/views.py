from django.shortcuts import render
from django.views.generic import CreateView
from users.forms import BenefactorSignUpForm, ProfileRegistrationDataSignUpForm, MemberSignUpForm, MemberForm
from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction

from django.http import HttpResponseRedirect


User = get_user_model()


@transaction.atomic
def register_benefactor(request):
    if request.method == 'POST':
        user_form = BenefactorSignUpForm(request.POST)
        profile_form = ProfileRegistrationDataSignUpForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            user.refresh_from_db()
            profile_form = ProfileRegistrationDataSignUpForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            messages.success(request, 'Conta criada com sucesso, faça login para continuar')
            return HttpResponseRedirect(reverse_lazy('core:home'))
        else:
            messages.error(request, 'Erro ao criar sua conta')
    else:
        user_form = BenefactorSignUpForm()
        profile_form = ProfileRegistrationDataSignUpForm()
    return render(request, 'registration/signup_form.html', {'user_form': user_form, 'profile_form': profile_form})


@transaction.atomic
def register_member(request):
    if request.method == 'POST':
        user_form = BenefactorSignUpForm(request.POST)
        profile_form = ProfileRegistrationDataSignUpForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            user.refresh_from_db()
            profile_form = ProfileRegistrationDataSignUpForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            messages.success(request, 'Conta criada com sucesso, faça login para continuar')
            return HttpResponseRedirect(reverse_lazy('core:home'))
        else:
            messages.error(request, 'Erro ao criar sua conta')
    else:
        user_form = MemberSignUpForm()
        member_form = MemberForm()
        profile_form = ProfileRegistrationDataSignUpForm()
    return render(request, 'registration/signup_form.html', 
    {'user_form': user_form, 'profile_form': profile_form, 'member_form': member_form})


# class BenefactorSignUpView(CreateView):
#     model = User
#     form_class = BenefactorSignUpForm
#     template_name = 'registration/signup_form.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'benefactor'
#         kwargs['form_profile'] = ProfileRegistrationDataSignUpForm()
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return HttpResponseRedirect(reverse_lazy('core:home'))
