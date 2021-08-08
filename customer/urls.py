from django.urls import path

from customer import views

urlpatterns = [
    path('list', views.CustomerListView.as_view(), name='customer_list'),
    path('create', views.CustomerCreateView.as_view(), name='customer_create'),
    path('<int:pk>', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/update', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('<int:pk>/delete', views.CustomerDeleteView.as_view(), name='customer_delete'),
]