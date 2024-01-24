from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_views_group(sender, instance, created, **kwargs):
    if created:
        try:
            view = Group.objects.get(name='visitante')
        except Group.DoesNotExist:
            view = Group.objects.create(name='visitante')
        instance.user.groups.add(view)