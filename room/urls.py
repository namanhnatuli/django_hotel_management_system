from django.urls import path
from room import views

urlpatterns = [
    path('facility/list', views.FacilityListView.as_view(), name='facility_list'),
    path('facility/create', views.FacilityCreateView.as_view(), name='facility_create'),
    path('facility/<int:pk>/update', views.FacilityUpdateView.as_view(), name='facility_update'),
    path('facility/<int:pk>/delete', views.FacilityDeleteView.as_view(), name='facility_delete'),

    path('class/list', views.RoomTypeListView.as_view(), name='roomtype_list'),
    path('class/create', views.RoomTypeCreateView.as_view(), name='roomtype_create'),
    path('class/<int:pk>/update', views.RoomTypeUpdateView.as_view(), name='roomtype_update'),
    path('class/<int:pk>/delete', views.RoomTypeDeleteView.as_view(), name='roomtype_delete'),

    path('list', views.RoomListView.as_view(), name='room_list'),
    path('create', views.RoomCreateView.as_view(), name='room_create'),
    path('<slug:pk>', views.RoomDetailView.as_view(), name='room_detail'),
    path('<slug:pk>/update', views.RoomUpdateView.as_view(), name='room_update'),
    path('<slug:pk>/delete', views.RoomDeleteView.as_view(), name='room_delete'),
]