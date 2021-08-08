from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

from booking.forms import BookingForm
from reservation.forms import ReservationForm, ReservationUpdateForm
from reservation.models import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation_list.html'


class ReservationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'reservation.view_reservation'
    model = Reservation
    template_name = 'reservation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = get_object_or_404(Reservation, id=self.kwargs['pk'])
        context['Total_guests'] = reservation.no_of_adults + reservation.no_of_children
        return context


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('reservation_list')


class ReservationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'reservation.change_reservation'
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = 'reservation_update.html'
    success_url = reverse_lazy('reservation_list')

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        form.instance.user = self.request.user
        reservation = super(ReservationUpdateView, self).form_valid(form)
        return reservation


def BookingCreatePopup(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_booking");</script>' % (instance.pk, instance))
    return render(request, "booking_form_popup.html", {"form": form})


class ReservationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'reservation.delete_reservation'
    model = Reservation
    template_name = 'reservation_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('reservation_list')
