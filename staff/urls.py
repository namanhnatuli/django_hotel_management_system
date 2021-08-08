from django.urls import path
from staff import views


urlpatterns = [
    path('department/list', views.StaffRoleListView.as_view(), name='staffrole_list'),
    path('department/<int:pk>/', views.StaffRoleDetailView.as_view(), name='staffrole_detail'),
    path('department/create', views.StaffRoleCreateView.as_view(), name='staffrole_create'),
    path('department/<int:pk>/update', views.StaffRoleUpdateView.as_view(), name='staffrole_update'),
    path('department/<int:pk>/delete', views.StaffRoleDeleteView.as_view(), name='staffrole_delete'),

    path('list', views.StaffListView.as_view(), name='staff_list'),
    path('create', views.StaffCreateView.as_view(), name='staff_create'),
    path('<slug:pk>', views.StaffDetailView.as_view(), name='staff_detail'),
    path('<slug:pk>/update', views.StaffUpdateView.as_view(), name='staff_update'),
    path('<slug:pk>/delete', views.StaffDeleteView.as_view(), name='staff_delete'),
]