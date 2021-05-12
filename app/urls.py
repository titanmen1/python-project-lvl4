from django.urls import path
from django.views.generic import TemplateView
from app import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('users/', views.UsersList.as_view(), name='users'),
    path('users/create/', views.CreateUser.as_view(), name='create'),
    path('users/<int:pk>/update/', views.EditUser.as_view(), name='edit_user'),
    path('users/<int:pk>/delete/', views.DelUser.as_view(), name='del_user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('statuses/', views.StatusesList.as_view(), name='statuses'),
    path('statuses/create/', views.StatusCreate.as_view(),
         name='create_status'),
    path('statuses/<int:pk>/update/', views.StatusEdit.as_view(),
         name='update_status'),
    path('statuses/<int:pk>/delete/', views.StatusDelete.as_view(),
         name='delete_status'),

    path('tasks/', views.TasksList.as_view(), name='tasks'),
    path('tasks/create/', views.TaskCreate.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', views.TaskEdit.as_view(),
         name='update_task'),
    path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(),
         name='delete_task'),

    path('labels/', views.LabelsList.as_view(), name='labels'),
    path('labels/create/', views.LabelCreate.as_view(),
         name='create_label'),
    path('labels/<int:pk>/update/', views.LabelEdit.as_view(),
         name='update_label'),
    path('labels/<int:pk>/delete/', views.LabelDelete.as_view(),
         name='delete_label'),
]
