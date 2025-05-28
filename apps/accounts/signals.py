from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from apps.employers.models import Employer


@receiver(post_save, sender=CustomUser)
def create_employer(sender, instance, created, **kwargs):
    if created and instance.enterprise:
        try:
            Employer.objects.create(
                name=f"{instance.first_name} {instance.last_name}".strip(),
                email=instance.email,
                phone=instance.phone or '',
                enterprise=instance.enterprise,
                user=instance,
                is_active=instance.is_active
            )
        except Exception as e:
            print(f"Error creating employer for user {instance.username}: {str(e)}") 