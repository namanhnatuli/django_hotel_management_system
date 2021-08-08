from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from booking.models import CheckIn
from room.forms import FacilityForm, RoomTypeForm, RoomForm
from room.models import Room, RoomType, Facility
# Create your views here.


class FacilityListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'room.view_facility'
    model = Facility
    template_name = 'facility_list.html'


class FacilityCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'room.add_facility'
    template_name = 'facility_form.html'
    model = Facility
    form_class = FacilityForm
    success_url = reverse_lazy('facility_list')


class FacilityDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'room.delete_facility'
    model = Facility
    template_name = 'facility_confirm_delete.html'
    success_url = reverse_lazy('facility_list')


class FacilityUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'room.change_facility'
    model = Facility
    form_class = FacilityForm
    template_name = 'facility_update.html'
    success_url = reverse_lazy('facility_list')


class RoomTypeListView(ListView):
    model = RoomType
    template_name = 'roomtype_list.html'


class RoomTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'room.add_roomtype'
    template_name = 'roomtype_form.html'
    model = RoomType
    form_class = RoomTypeForm
    success_url = reverse_lazy('roomtype_list')


class RoomTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'room.delete_roomtype'
    model = RoomType
    template_name = 'roomtype_confirm_delete.html'
    success_url = reverse_lazy('roomtype_list')


class RoomTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'room.change_roomtype'
    model = RoomType
    form_class = RoomTypeForm
    template_name = 'roomtype_update.html'
    success_url = reverse_lazy('roomtype_list')


class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_checkin'] = CheckIn.objects.filter(checkout=None)
        return context


class RoomDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'room.view_room'
    model = Room
    template_name = 'room_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_checkin'] = CheckIn.objects.filter(checkout=None)
        return context


class RoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'room.add_room'
    template_name = 'room_form.html'
    model = Room
    form_class = RoomForm
    success_url = reverse_lazy('room_list')


class RoomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'room.delete_room'
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')


class RoomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'room.change_room'
    model = Room
    form_class = RoomForm
    template_name = 'room_update.html'
    success_url = reverse_lazy('room_list')

