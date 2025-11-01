from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.generic import ListView, DetailView, CreateView
from .models import Shipment, Order
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  
from django.urls import reverse_lazy, reverse
from django.views import View


class ShipmentListView(ListView):
    model = Shipment
    template_name = 'logistics/shipment_list.html'
    context_object_name = 'shipment_list'

    def get_queryset(self):
        return Shipment.objects.all()  # ✅ Ensures shipments are loaded

def shipment_list(request):
    shipments = Shipment.objects.all()  # Fetch all shipments
    return render(request, 'logistics/shipments.html', {'shipments': shipments})

class ShipmentDetailView(DetailView):
    model = Shipment
    template_name = 'logistics/shipment_detail.html'
    context_object_name = 'shipment'

class OrderCreateView(CreateView):
    model = Order
    fields = ['customer_name', 'order_date', 'total_cost', 'status']
    template_name = 'logistics/order_form.html'
    success_url = reverse_lazy('order_list')

class OrderDetailView(DetailView):
    model = Order
    template_name = "logistics/order_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract field names in Python instead of using _meta in the template
        context['status_choices'] = Order._meta.get_field('status').choices  # Pass choices
        return context

class OrderListView(ListView):
    model = Order
    template_name = 'logistics/order_list.html'  # Ensure this template exists
    context_object_name = 'orders'

class OrderStatusUpdateView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get("status")  # Get the selected status

        if new_status in dict(Order._meta.get_field('status').choices):  # Validate status
            order.status = new_status
            order.save()

        return HttpResponseRedirect(reverse("order_detail", args=[pk])) 
    
def dashboard(request):
    shipment_list = Shipment.objects.all()
    order_list = Order.objects.all()
    return render(request, 'logistics/dashboard.html', {'shipment_list': shipment_list, 'order_list': order_list})

def dashboard_view(request):
    total_orders = Order.objects.count()
    pending_shipments = Shipment.objects.filter(status="Pending").count()
    completed_shipments = Shipment.objects.filter(status="Delivered").count()

    context = {
        "total_orders": total_orders,
        "pending_shipments": pending_shipments,
        "completed_shipments": completed_shipments,
    }

    return render(request, "dashboard.html", context)

def welcome(request):
    return render(request, 'logistics/landing.html')

def my_logout_view(request):
    print("Logout function called")  # This should appear in the terminal
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)  
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to your home/dashboard page
    else:
        form = UserCreationForm()
    return render(request, "logistics/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")  # Redirect to your main page
    else:
        form = AuthenticationForm()
    return render(request, "logistics/login.html", {"form": form})
