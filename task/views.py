from datetime import timedelta

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, decorators
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Task, TaskUser
from .tasks import send_task_notify_mail
from .forms import TaskForm, TaskUserAttachForm
from comment.models import Comment


User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    template_name = "task/list.html"
    context_object_name = 'tasks'

    def get_queryset(self):
        attached = TaskUser.objects.filter(user=self.request.user).values_list('task', flat=True)
        attached_tasks = Task.objects.filter(pk__in=attached)

        user_tasks = Task.objects.filter(author=self.request.user).order_by('deadline')
        return user_tasks.union(attached_tasks)


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = "task/detail.html"
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        task = self.get_object()
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task_id=self.get_object().id).order_by('created_at')
        context['comment_perm'] = True

        if self.request.user != task.author:
            task_user = TaskUser.objects.get(user=self.request.user, task=task)
            context['comment_perm'] = task_user.access_type == TaskUser.COMMENT

        return context

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or TaskUser.objects.filter(user=self.request.user, task=task).count()


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


@decorators.login_required
def attach(request, pk):
    task = get_object_or_404(Task, pk=pk, author=request.user)
    users = TaskUser.objects.filter(task=task)

    if request.method == 'POST':
        form = TaskUserAttachForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            access_type = form.cleaned_data.get('access')

            try:
                TaskUser.objects.get(user=user, task=task)
                messages.warning(request, 'User already has access to this task.')
                return render(request, 'task/attach.html', {'task': task, 'form': form, 'users': users})
            except TaskUser.DoesNotExist:
                TaskUser.objects.create(user=user, access_type=access_type, task=task)
                send_task_notify_mail.apply_async((task.title, task.author.username, user.email),
                                                  eta=task.deadline - timedelta(minutes=10))
                messages.success(request, 'Access successfully granted.')
                return redirect('task:user-attach', pk=pk)

    else:
        form = TaskUserAttachForm()

    return render(request, 'task/attach.html', {'task': task, 'form': form, 'users': users})
