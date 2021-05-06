from django.urls import path
from django.views.generic import TemplateView
from task_manager.views import UsersList, CreateUser, LoginView, EditUser, DelUser, LogoutView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('users/', UsersList.as_view(), name='users'),
    path('users/create/', CreateUser.as_view(), name='create'),
    path('users/<int:pk>/update/', EditUser.as_view(), name='edit_user'),
    path('users/<int:pk>/delete/', DelUser.as_view(), name='del_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]