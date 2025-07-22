# patient/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(pre_save, sender=UserProfile)
def log_user_role(sender, instance, **kwargs):
    print(f" Pre-saving profile for: {instance.user.username}")
    print(f"Role selected: {instance.role}")
