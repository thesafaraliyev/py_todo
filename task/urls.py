from django.urls import path, include

from . import views

app_name = 'task'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:pk>/', include([
        path('', views.TaskDetailView.as_view(), name='detail'),
        path('update/', views.TaskUpdateView.as_view(), name='update'),
        path('delete/', views.TaskDeleteView.as_view(), name='delete'),
        path('attach/', views.attach, name='user-attach'),
        path('comment/', views.attach, name='add-comment'),
    ]))
]
