from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from task_manager.forms import UserForm


class UsersList(ListView):
    template_name = "users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'register.html'
    fields = ['first_name', 'last_name', 'username',  'email', 'password']
    success_message = _('You are create new user')

    def get_success_url(self):
        return reverse('login')


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = _('You are logged in')

    def get_success_url(self):
        return reverse('index')


class LogoutView(LogoutView):
    def get_success_url(self):
        return reverse('index')


class EditUser(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'edit_user.html'
    form_class = UserForm

    permission_denied_message = _('You do not have permission to modify another user.')
    permission_denied_url = reverse_lazy('users')

    def test_func(self):
        user = self.get_object()
        return user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)


class DelUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'del_user.html'
    permission_denied_message = _('You do not have permission to delete another user.')
    permission_denied_url = reverse_lazy('users')
    success_message = _('User deleted')

    def get_success_url(self):
        return reverse('index')

    def test_func(self):
        user = self.get_object()
        return user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)
