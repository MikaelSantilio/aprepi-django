from django.views.generic import TemplateView
from django.contrib.auth.mixins import AccessMixin


class EmployeeRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        elif not request.user.is_employee:
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

    template_name = "core/home.html"
