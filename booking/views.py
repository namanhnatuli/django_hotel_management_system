from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from booking import forms
from booking.models import Booking, CheckIn, Service, CheckOut
from customer.forms import CustomerForm
from customer.models import Customer
import json

from room.models import Room


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service_list.html'


class ServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'booking.add_service'
    template_name = 'service_form.html'
    model = Service
    form_class = forms.ServiceForm
    success_url = reverse_lazy('service_list')


class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'booking.delete_service'
    model = Service
    template_name = 'service_confirm_delete.html'
    success_url = reverse_lazy('service_list')


class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.change_service'
    model = Service
    form_class = forms.ServiceForm
    template_name = 'service_update.html'
    success_url = reverse_lazy('service_list')


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking_list.html'


class BookingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'booking.view_booking'
    model = Booking
    template_name = 'booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = get_object_or_404(Booking, id=self.kwargs['pk'])
        context['Total_guests'] = reservation.no_of_adults + reservation.no_of_children
        return context


class BookingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'booking.add_booking'
    model = Booking
    form_class = forms.BookingForm
    template_name = 'booking_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.booking_date_time = timezone.now()
        form.instance.updated_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('booking_list')


def CustomerCreatePopup(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_customer");</script>' % (instance.pk, instance))
    return render(request, "customer_form_popup.html", {"form": form})


@csrf_exempt
def get_customer_id(request):
    if request.is_ajax():
        customer_name = request.GET['customer_name']
        customer_id = Customer.objects.get(name=customer_name).id
        data = {'customer_id': customer_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


class BookingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.change_booking'
    model = Booking
    form_class = forms.BookingUpdateForm
    template_name = 'booking_update.html'

    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.object.id)
        form.instance.updated_at = timezone.now()
        form.instance.user = self.request.user
        form.instance.booking_date_time = booking.booking_date_time
        form.instance.customer = booking.customer
        form.instance.booking_type = booking.booking_type
        return super(BookingUpdateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('booking_detail', args=[str(self.object.id)])


class BookingCancelView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.change_booking'
    model = Booking
    form_class = forms.BookingCancelRequestForm
    template_name = 'booking_cancel.html'

    def form_valid(self, form):
        form.instance.canceled = True
        form.instance.updated_at = timezone.now()
        return super(BookingCancelView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('booking_detail', args=[str(self.object.id)])


class BookingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'booking.delete_booking'
    model = Booking
    template_name = 'booking_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('booking_list')


class CheckinCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'booking.add_checkin'
    model = CheckIn
    form_class = forms.CheckInForm
    template_name = 'checkin_form.html'
    success_url = reverse_lazy('checkin_list')

    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.kwargs['pk'])
        form.instance.id = booking.id
        form.instance.booking = booking
        form.instance.user = self.request.user
        form.instance.checkin_time = timezone.now()
        form.instance.updated_at = timezone.now()
        form.save()
        checkin = super(CheckinCreateView, self).form_valid(form)
        for room in form.cleaned_data.get('rooms'):
            room.availability = False
            room.save()
        return checkin


class CheckinListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'booking.view_checkin'
    model = CheckIn
    template_name = 'checkin_list.html'
    queryset = CheckIn.objects.all().order_by('-checkin_time')


class CheckinDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'booking.view_checkin'
    model = CheckIn
    template_name = 'checkin_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservation = get_object_or_404(Booking, id=self.kwargs['pk'])
        context['Total_guests'] = reservation.no_of_adults + reservation.no_of_children
        return context


class CheckinUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.change_checkin'
    model = CheckIn
    form_class = forms.CheckInForm
    template_name = 'checkin_update.html'

    def form_valid(self, form):
        form.instance.updated_at = timezone.now()
        form.instance.user = self.request.user
        rooms_number = [room.room_number for room in self.object.rooms.all()]
        form.save()
        checkin = super(CheckinUpdateView, self).form_valid(form)
        for room in Room.objects.filter(Q(room_number__in=rooms_number) | (Q(availability=True) & Q(maintenance=False))):
            if room in form.cleaned_data.get('rooms'):
                room.availability = False
                self.object.rooms.add(room)
            else:
                room.availability = True
                self.object.rooms.filter(room_number=room.room_number).delete()
            room.save()
        return checkin

    def get_success_url(self, **kwargs):
        return reverse_lazy('checkin_detail', args=[str(self.object.id)])


class CheckinDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'booking.delete_checkin'
    model = CheckIn
    template_name = 'checkin_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('checkin_list')


class CheckoutCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'booking.add_checkout'
    model = CheckOut
    form_class = forms.CheckOutForm
    template_name = 'checkout_form.html'
    success_url = reverse_lazy('checkout_list')

    def form_valid(self, form):
        checkin = get_object_or_404(CheckIn, id=self.kwargs['pk'])
        form.instance.id = checkin.id
        form.instance.checkin = checkin
        form.instance.checkout_time = timezone.now()
        form.instance.checkout_by = self.request.user
        checkout = super(CheckoutCreateView, self).form_valid(form)
        for room in checkin.rooms.all():
            room.availability = True
            room.save()
        return checkout


class CheckoutListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'booking.view_checkout'
    model = CheckOut
    template_name = 'checkout_list.html'


class CheckoutDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'booking.view_checkout'
    model = CheckOut
    template_name = 'checkout_detail.html'


class CheckoutUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'booking.change_checkout'
    model = CheckOut
    form_class = forms.CheckOutForm
    template_name = 'checkout_update.html'


class CheckoutDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'booking.delete_checkout'
    model = CheckOut
    template_name = 'checkout_confirm_delete.html'
    success_url = reverse_lazy('checkout_list')
