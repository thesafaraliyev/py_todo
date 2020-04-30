from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.simple_tag
def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'
