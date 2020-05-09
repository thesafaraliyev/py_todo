from django import forms
from django.db.models import Q
from django.contrib.auth import get_user_model

from tempus_dominus.widgets import DateTimePicker

from .models import Task, TaskUser

User = get_user_model()


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
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TaskUserAttachForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or email'}))
    access = forms.ChoiceField(label='Access type', choices=TaskUser.ACCESS_TYPES)

    def clean_user(self):
        identifier = self.cleaned_data.get('user')
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        if not user:
            raise forms.ValidationError('User is not found.', 400)

        return user
