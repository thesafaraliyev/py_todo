from django.urls import path
from . import views

app_name = 'task'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('<int:pk>/udapte', views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='delete'),
    # path('<int:task_id>/attach_user', views.attach_user, name='attach_user'),
    # path('<int:task_id>/add_comment', views.add_comment, name='add_comment'),
]