from .models import Order, Shipment

def dashboard_data(request):
    if request.user.is_authenticated:
        return {
            "total_orders": Order.objects.count(),
            "pending_shipments": Shipment.objects.filter(status="Pending").count(),
            "completed_shipments": Shipment.objects.filter(status="Delivered").count(),
        }
    return {}  # Return empty dict if user is not logged in
