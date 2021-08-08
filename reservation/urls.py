from django.urls import path
from . import views
from reservation import views


urlpatterns = [
    path('list', views.ReservationListView.as_view(), name='reservation_list'),
    path('create', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('<int:pk>', views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('<int:pk>/processing', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('<int:pk>/delete', views.ReservationDeleteView.as_view(), name='reservation_delete'),

    path('booking/create', views.BookingCreatePopup, name="BookingCreate"),
]