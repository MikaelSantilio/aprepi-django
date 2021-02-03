from core.views import EmployeeRequiredMixin, SuperuserRequiredMixin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from users.forms import ProfileForm, SignUpForm, MemberForm, VoluntaryForm
from users.models import Benefactor

User = get_user_model()


class FormErrorMessageMixin():

    def send_form_error_messages(self, request, messages, *args):

        for form in args:
            if form.is_valid():
                continue

            for key, value in form.errors.items():
                for e in value:
                    messages.warning(request, f"{key} - {e}")


class MemberSignUpView(EmployeeRequiredMixin, TemplateResponseMixin, FormErrorMessageMixin, ContextMixin, View):

    template_name = 'registration/signup_form_member.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = SignUpForm()
        member_form = MemberForm()
        profile_form = ProfileForm()

        context['user_form'] = user_form
        context['form_action'] = reverse_lazy("users:signup-member")
        context['member_form'] = member_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        member_form = MemberForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and member_form.is_valid():
            return self.form_valid(user_form)
        else:
            self.send_form_error_messages(request, messages, user_form, profile_form, member_form)

            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    @transaction.atomic
    def form_valid(self, user_form):
        user = user_form.save(commit=False)
        user.is_member = True
        user.save()
        user.refresh_from_db()

        profile_form = ProfileForm(self.request.POST, instance=user.profile)
        profile_form.full_clean()
        profile_form.save()

        member_form = MemberForm(self.request.POST, instance=user.member)
        member_form.full_clean()
        member_form.save()

        messages.success(self.request, 'Conta de sócio criada com sucesso')

        return HttpResponseRedirect(reverse_lazy('core:home'))


class BenefactorSignUpView(TemplateResponseMixin, FormErrorMessageMixin, ContextMixin, View):

    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = SignUpForm()
        profile_form = ProfileForm()

        context['form_action'] = reverse_lazy("users:signup-benefactor")
        context['user_form'] = user_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form)
        else:
            self.send_form_error_messages(request, messages, user_form, profile_form)

            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('core:home'))
        return self.render_to_response(self.get_context_data())

    @transaction.atomic
    def form_valid(self, user_form):
        user = user_form.save(commit=False)
        user.is_benefactor = True
        user.save()
        user.refresh_from_db()

        profile_form = ProfileForm(self.request.POST)
        profile_form.full_clean()
        profile_form.instance.user = user
        profile_form.save()

        Benefactor.objects.create(user=user)
        messages.success(self.request, 'Conta criada com sucesso, faça login para continuar')

        return HttpResponseRedirect(reverse_lazy('users:login'))


class EmployeeSignUpView(SuperuserRequiredMixin, TemplateResponseMixin, FormErrorMessageMixin, ContextMixin, View):

    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = SignUpForm()
        profile_form = ProfileForm()

        context['form_action'] = reverse_lazy("users:signup-employee")
        context['user_form'] = user_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form)
        else:
            self.send_form_error_messages(request, messages, user_form, profile_form)

            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    @transaction.atomic
    def form_valid(self, user_form):
        user = user_form.save(commit=False)

        user.is_employee = True
        user.save()
        user.refresh_from_db()

        profile_form = ProfileForm(self.request.POST, instance=user.profile)
        profile_form.full_clean()
        profile_form.save()

        messages.success(self.request, 'Conta de funcionário criada com sucesso')

        return HttpResponseRedirect(reverse_lazy('core:home'))


class VoluntarySignUpView(EmployeeRequiredMixin, TemplateResponseMixin, FormErrorMessageMixin, ContextMixin, View):

    template_name = 'registration/signup_form_voluntary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = SignUpForm()
        voluntary_form = VoluntaryForm()
        profile_form = ProfileForm()

        context['user_form'] = user_form
        context['form_action'] = reverse_lazy("users:signup-voluntary")
        context['voluntary_form'] = voluntary_form
        context['profile_form'] = profile_form

        return context

    def post(self, request, *args, **kwargs):

        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        voluntary_form = VoluntaryForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and voluntary_form.is_valid():
            return self.form_valid(user_form)
        else:
            self.send_form_error_messages(request, messages, user_form, profile_form, voluntary_form)

            return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    @transaction.atomic
    def form_valid(self, user_form):
        user = user_form.save(commit=False)
        user.is_voluntary = True
        user.save()
        user.refresh_from_db()

        profile_form = ProfileForm(self.request.POST, instance=user.profile)
        profile_form.full_clean()
        profile_form.save()

        voluntary_form = VoluntaryForm(self.request.POST, instance=user.voluntary)
        voluntary_form.full_clean()
        voluntary_form.save()

        messages.success(self.request, 'Conta de voluntário criada com sucesso')

        return HttpResponseRedirect(reverse_lazy('core:home'))
