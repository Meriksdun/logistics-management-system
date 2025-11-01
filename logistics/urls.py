# logistics/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from .views import signup, login_view, my_logout_view, OrderDetailView, OrderListView, shipment_list
from . import views

urlpatterns = [
    path('shipments/', views.ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/', shipment_list, name='shipment_list'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment_detail'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update-status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='logistics/login.html'), name='login'),
    path('logout/', my_logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.welcome, name='welcome'),
]