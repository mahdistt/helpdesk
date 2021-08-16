# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserRegisterForm


class SignUpView(SuccessMessageMixin, CreateView):
    """
    Register user to website financial
    """
    template_name = 'user/create-signup.html'
    success_url = reverse_lazy('dashboard:dashboard')
    form_class = UserRegisterForm
    success_message = "%(username)s Your profile was created successfully"


class LogoutView(SuccessMessageMixin, LogoutView):
    template_name = 'user/LogoutView_form.html'
    success_url = reverse_lazy('user:login-user')
    success_message = "Good Bye %(username)s "


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'user/LoginView_form.html'
    success_url = reverse_lazy('dashboard:dashboard')
    success_message = "Welcome %(username)s "


class EditProfile(LoginRequiredMixin, UpdateView):
    """
    Updates a user profile
    """
    model = get_user_model()
    fields = (
        'first_name',
        'last_name',
        'email',
    )
    template_name = 'user/edit-profile.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def get_object(self, queryset=None):
        return self.request.user
