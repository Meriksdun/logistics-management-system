from django.contrib import admin
from .models import Order, Shipment, Vehicle, CustomUser

admin.site.register(Order)
admin.site.register(Shipment)
admin.site.register(Vehicle)
admin.site.register(CustomUser)
