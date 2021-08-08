from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from customer.forms import CustomerForm
from customer.models import Customer


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'customer.view_customer'
    model = Customer
    template_name = 'customer_list.html'


class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'customer.view_customer'
    model = Customer
    template_name = 'customer_detail.html'


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'customer.add_customer'
    template_name = 'customer_form.html'
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'customer.delete_customer'
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'customer.change_customer'
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_update.html'
    success_url = reverse_lazy('customer_list')
