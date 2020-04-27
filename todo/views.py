from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from task.models import Task
from .forms import TodoUserAttachForm
from .models import Todo
from django.contrib import messages

User = get_user_model()


@login_required
def attach(request, pk):
    task = get_object_or_404(Task, pk=pk, author=request.user)
    attached_users = Todo.objects.filter(task=task)

    if request.method == 'POST':
        form = TodoUserAttachForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            access_type = form.cleaned_data.get('access')

            try:
                Todo.objects.get(user=user, task=task)
                messages.warning(request, 'User already has access to this task.')
                return render(request, 'todo/attach.html',
                              {'task': task, 'form': form, 'attached_users': attached_users})
            except Todo.DoesNotExist:
                Todo.objects.create(user=user, access_type=access_type, task=task)
                messages.success(request, 'Access successfully granted.')
                return redirect('todo:attach', pk=pk)

    else:
        form = TodoUserAttachForm()

    return render(request, 'todo/attach.html', {'task': task, 'form': form, 'attached_users': attached_users})


@login_required
def list(request):
    todo_list = Todo.objects.filter(user=request.user)
    return render(request, 'todo/list.html', {'todo_list': todo_list})

# class TaskListView(LoginRequiredMixin, ListView):
#     template_name = "task/list.html"
#     context_object_name = 'tasks'
#
#     def get_queryset(self):
#         return Task.objects.filter(author=self.request.user).order_by('deadline')
#
#
# class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = Task
#     template_name = "task/detail.html"
#     context_object_name = 'task'
#
#     def test_func(self):
#         task = self.get_object()
#         return self.request.user == task.author
#
#
# class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Task
#     template_name = 'task/create.html'
#     form_class = TaskForm
#     success_url = reverse_lazy('task:list')
#     success_message = 'New task successfully created!'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#
#
# class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
#     model = Task
#     template_name = 'task/update.html'
#     form_class = TaskForm
#     success_url = reverse_lazy('task:list')
#     success_message = 'Task successfully updated!'
#
#     def test_func(self):
#         task = self.get_object()
#         return self.request.user == task.author
#
#
# class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
#     model = Task
#     template_name = 'task/delete.html'
#     success_url = reverse_lazy('task:list')
#     success_message = 'Task successfully deleted!'
#
#     def test_func(self):
#         task = self.get_object()
#         return self.request.user == task.author
