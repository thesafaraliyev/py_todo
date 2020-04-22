# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy


class TaskListView(ListView):
    model = Task
    template_name = "task/list.html"
    context_object_name = 'tasks'
    queryset = Task.objects.all().order_by('deadline')


class TaskDetailView(DetailView):
    model = Task
    template_name = "task/detail.html"
    context_object_name = 'task'


class TaskCreateView(SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'task/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:list')
    success_message = 'New task successfully created!'


class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:list')
    success_message = 'Task successfully updated!'


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('task:list')
    success_message = 'Task successfully deleted!'
