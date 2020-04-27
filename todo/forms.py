from django import forms
from .models import Todo
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class TodoUserAttachForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or email'}))
    access = forms.ChoiceField(label='Access type', choices=Todo.ACCESS_TYPES)

    def clean_user(self):
        identifier = self.cleaned_data.get('user')
        user = User.objects.filter(Q(username=identifier) | Q(email=identifier)).first()
        if not user:
            raise forms.ValidationError('User is not found.', 400)

        return user
