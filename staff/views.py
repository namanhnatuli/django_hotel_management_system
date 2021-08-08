from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView

from staff.forms import StaffForm, StaffRoleForm
from staff.models import Staff, StaffRole


class StaffRoleListView(LoginRequiredMixin, ListView):
    model = StaffRole
    template_name = 'staffrole_list.html'


class StaffRoleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'staff.view_staffrole'
    model = StaffRole
    template_name = 'staffrole_detail.html'


class StaffRoleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'room.add_staffrole'
    template_name = 'staffrole_form.html'
    model = StaffRole
    form_class = StaffRoleForm
    success_url = reverse_lazy('staffrole_list')


class StaffRoleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'room.delete_staffrole'
    model = StaffRole
    template_name = 'staffrole_confirm_delete.html'
    success_url = reverse_lazy('staffrole_list')


class StaffRoleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'room.change_staffrole'
    model = StaffRole
    form_class = StaffRoleForm
    template_name = 'staffrole_update.html'
    success_url = reverse_lazy('staffrole_list')


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff_list.html'


class StaffDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'staff.view_staff'
    model = Staff
    template_name = 'staff_detail.html'


class StaffCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'staff.add_staff'
    template_name = 'staff_form.html'
    model = Staff
    form_class = StaffForm
    success_url = reverse_lazy('staff_list')


class StaffDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'staff.delete_staff'
    model = Staff
    template_name = 'staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')


class StaffUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'staff.change_staff'
    model = Staff
    form_class = StaffForm
    template_name = 'staff_update.html'
    success_url = reverse_lazy('staff_list')
