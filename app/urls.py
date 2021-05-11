from django.urls import path
from django.views.generic import TemplateView
from app.views import UsersList, CreateUser, LoginView, EditUser, DelUser, LogoutView, StatusesList, \
    StatusEdit, StatusDelete, StatusCreate, TasksList, TaskEdit, TaskDelete, TaskCreate, LabelsList, LabelCreate, \
    LabelEdit, LabelDelete

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('users/', UsersList.as_view(), name='users'),
    path('users/create/', CreateUser.as_view(), name='create'),
    path('users/<int:pk>/update/', EditUser.as_view(), name='edit_user'),
    path('users/<int:pk>/delete/', DelUser.as_view(), name='del_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('statuses/', StatusesList.as_view(), name='statuses'),
    path('statuses/create/', StatusCreate.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', StatusEdit.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', StatusDelete.as_view(), name='delete_status'),

    path('tasks/', TasksList.as_view(), name='tasks'),
    path('tasks/create/', TaskCreate.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', TaskEdit.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', TaskDelete.as_view(), name='delete_task'),

    path('labels/', LabelsList.as_view(), name='labels'),
    path('labels/create/', LabelCreate.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', LabelEdit.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', LabelDelete.as_view(), name='delete_label'),
]