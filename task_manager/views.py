import datetime

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
from task_manager.models import Status, Task


class UsersList(ListView):
    template_name = "users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserForm
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

    def delete(self, request, *args, **kwargs):
        if self.get_object().executor.all().exists() or self.get_object().author.all().exists():
            messages.error(self.request, _('Unable to delete user because it is in use'))
            return redirect('users')
        return super().delete(request, *args, **kwargs)


class StatusesList(ListView):
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"

    def get_queryset(self):
        return Status.objects.all()


class StatusCreate(SuccessMessageMixin, CreateView):
    model = Status
    template_name = "statuses/statuses_create.html"
    fields = ['name']
    success_message = _('You are create new status')

    def get_success_url(self):
        return reverse('statuses')


class StatusEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    template_name = "statuses/statuses_edit.html"
    fields = ['name']
    success_message = _('You are update status')

    def get_success_url(self):
        return reverse('statuses')


class StatusDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "statuses/statuses_delete.html"
    success_message = _('Status deleted')

    def get_success_url(self):
        return reverse('statuses')

    def delete(self, request, *args, **kwargs):
        if self.get_object().status.all().exists():
            messages.error(self.request, _('Unable to delete status because it is in use'))
            return redirect('statuses')
        return super().delete(request, *args, **kwargs)


class TasksList(ListView):
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.all()


class TaskCreate(SuccessMessageMixin, CreateView):
    model = Task
    template_name = "tasks/tasks_create.html"
    fields = ['name', 'status', 'description']
    success_message = _('You are create new tasks')

    def get_success_url(self):
        return reverse('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = "tasks/tasks_edit.html"
    fields = ['name', 'status', 'description']
    success_message = _('You are update task')

    def get_success_url(self):
        return reverse('tasks')


class TaskDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/tasks_delete.html"
    success_message = _('task deleted')

    def get_success_url(self):
        return reverse('tasks')

    def delete(self, request, *args, **kwargs):
        print(self.get_object().author, request.user)
        if self.get_object().author != request.user:
            messages.error(self.request, _('Unable to delete task because this task created not you'))
            return redirect('tasks')
        return super().delete(request, *args, **kwargs)
