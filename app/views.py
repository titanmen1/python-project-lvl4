from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from app.filter import TaskFilter
from app.forms import UserForm, TaskForm
from app.mixins import CheckUserForDelMixin
from app.models import Status, Task, Label
from django_filters.views import FilterView


class UsersList(ListView):
    model = get_user_model()
    template_name = "users/users.html"
    context_object_name = "users"


class CreateUser(SuccessMessageMixin, CreateView):
    model = get_user_model()
    template_name = 'users/register.html'
    form_class = UserForm
    success_message = _('User successfully registered')

    def get_success_url(self):
        return reverse('login')


class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = _('You are logged in')

    def get_success_url(self):
        return reverse('index')


class LogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)


class EditUser(LoginRequiredMixin, CheckUserForDelMixin,
               SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/edit_user.html'
    form_class = UserForm
    success_message = _('User successfully updated')
    permission_denied_url = reverse_lazy('users')
    permission_denied_message = _('You do not have permission to modify another user.')

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)

    def get_success_url(self):
        return reverse('users')


class DelUser(LoginRequiredMixin, CheckUserForDelMixin,
              SuccessMessageMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/del_user.html'
    success_message = _('User deleted')
    permission_denied_url = reverse_lazy('users')
    permission_denied_message = _('You do not have permission to modify another user.')

    def get_success_url(self):
        return reverse('users')

    def handle_no_permission(self):
        messages.error(self.request, self.get_permission_denied_message())
        return redirect(self.permission_denied_url)

    def delete(self, request, *args, **kwargs):
        if self.get_object().executor.all().exists() \
                or self.get_object().author.all().exists():
            messages.error(self.request, _(
                'Unable to delete user because it is in use'))
            return redirect('users')
        messages.success(self.request, _('User deleted'))
        return super().delete(request, *args, **kwargs)


class StatusesList(LoginRequiredMixin, ListView):
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"

    def get_queryset(self):
        return Status.objects.all()


class StatusCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            messages.error(self.request, _(
                'Unable to delete status because it is in use'))
            return redirect('statuses')
        messages.success(self.request, _('Status successfully deleted'))
        return super().delete(request, *args, **kwargs)


class TasksList(LoginRequiredMixin, FilterView):
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter


class TaskCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = "tasks/tasks_create.html"
    form_class = TaskForm
    success_message = _('You are create new tasks')

    def get_success_url(self):
        return reverse('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = "tasks/tasks_edit.html"
    fields = ['name', 'status', 'description', 'executor', 'labels']
    success_message = _('You are update task')

    def get_success_url(self):
        return reverse('tasks')


class TaskDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "tasks/tasks_delete.html"
    success_message = _('Task deleted')

    def get_success_url(self):
        return reverse('tasks')

    def delete(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(self.request, _(
                'Unable to delete task because this task created not you'))
            return redirect('tasks')
        messages.success(self.request, _('Task successfully deleted'))
        return super().delete(request, *args, **kwargs)


class LabelsList(LoginRequiredMixin, ListView):
    template_name = "labels/label_list.html"
    context_object_name = "labels"

    def get_queryset(self):
        return Label.objects.all()


class LabelCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = "labels/label_create.html"
    fields = ['name']
    success_message = _('You are create new label')

    def get_success_url(self):
        return reverse('labels')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class LabelEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    template_name = "labels/label_edit.html"
    fields = ['name']
    success_message = _('You are update label')

    def get_success_url(self):
        return reverse('labels')


class LabelDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "labels/label_delete.html"
    success_message = _('Label deleted')

    def get_success_url(self):
        return reverse('labels')

    def delete(self, request, *args, **kwargs):
        if self.get_object().labels.all().exists():
            messages.error(self.request, _(
                'Unable to delete label because it is in use'))
            return redirect('labels')
        messages.success(self.request, _('Label successfully deleted'))
        return super().delete(request, *args, **kwargs)
