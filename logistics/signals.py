from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Shipment
import uuid

@receiver(post_save, sender=Order)
def create_shipment(sender, instance, created, **kwargs):
    if created:  # Only create shipment when order is newly created
        Shipment.objects.create(
            order=instance,
            tracking_number=str(uuid.uuid4())[:10],  # Generate a unique tracking number
        )
