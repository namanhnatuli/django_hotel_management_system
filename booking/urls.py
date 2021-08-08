from django.urls import path
from . import views

urlpatterns = [
    path('list', views.BookingListView.as_view(), name='booking_list'),
    path('create', views.BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>', views.BookingDetailView.as_view(), name='booking_detail'),
    path('<int:pk>/update', views.BookingUpdateView.as_view(), name='booking_update'),
    path('<int:pk>/delete', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('<int:pk>/cancel', views.BookingCancelView.as_view(), name='booking_cancel'),

    path('checkin/list', views.CheckinListView.as_view(), name='checkin_list'),
    path('<int:pk>/checkin', views.CheckinCreateView.as_view(), name='checkin_create'),
    path('<int:pk>/checkin/detail', views.CheckinDetailView.as_view(), name='checkin_detail'),
    path('<int:pk>/checkin/update', views.CheckinUpdateView.as_view(), name='checkin_update'),
    path('<int:pk>/checkin/delete', views.CheckinDeleteView.as_view(), name='checkin_delete'),

    path('checkout/list', views.CheckoutListView.as_view(), name='checkout_list'),
    path('<int:pk>/checkout', views.CheckoutCreateView.as_view(), name='checkout_create'),
    path('<int:pk>/checkout/detail', views.CheckoutDetailView.as_view(), name='checkout_detail'),
    path('<int:pk>/checkout/update', views.CheckoutUpdateView.as_view(), name='checkout_update'),
    path('<int:pk>/checkout/delete', views.CheckoutDeleteView.as_view(), name='checkout_delete'),

    path('customer/create', views.CustomerCreatePopup, name="CustomerCreate"),
    path('customer/ajax/get_customer_id', views.get_customer_id, name="get_customer_id"),

    path('service/list', views.ServiceListView.as_view(), name='service_list'),
    path('service/create', views.ServiceCreateView.as_view(), name='service_create'),
    path('service/<int:pk>/update', views.ServiceUpdateView.as_view(), name='service_update'),
    path('service/<int:pk>/delete', views.ServiceDeleteView.as_view(), name='service_delete'),
]