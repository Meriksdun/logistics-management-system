from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid  # For generating tracking numbers
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):  
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Completed", "Completed"),
    ]

    customer_name = models.CharField(max_length=255)
    order_date = models.DateField(default=timezone.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class Shipment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    tracking_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4)  # Auto-generate tracking number
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    estimated_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Shipment {self.tracking_number} - {self.status}"

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=255)

    def __str__(self):
        return self.vehicle_number

@receiver(post_save, sender=Order)
def create_shipment(sender, instance, created, **kwargs):
    if created:
        Shipment.objects.create(order=instance, status="Pending")