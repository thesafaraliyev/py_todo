from django import forms
from .models import Task
from tempus_dominus.widgets import DateTimePicker


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )

    class Meta:
        model = Task
        fields = ['title', 'deadline', 'description']
