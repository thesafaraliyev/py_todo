from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from todo.models import Todo

User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    template_name = "task/list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user).order_by('deadline')


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = "task/detail.html"
    context_object_name = 'task'

    # todo_list = Todo.objects.get(task=4)

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'task/create.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:list')
    success_message = 'New task successfully created!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:list')
    success_message = 'Task successfully updated!'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('task:list')
    success_message = 'Task successfully deleted!'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author
