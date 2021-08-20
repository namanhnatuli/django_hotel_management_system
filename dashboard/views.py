from calendar import monthrange

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from booking.models import CheckOut, CheckIn, Booking, BookingType
from customer.models import Customer
from dashboard.forms import NewUserForm, ProfileForm, form_validation_error
from dashboard.models import Profile
from reservation.models import Reservation
from room.models import Room, RoomType
from staff.models import Staff, StaffRole
from datetime import datetime
from dateutil.relativedelta import *


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):

        NOW = datetime.now()
        last_month = NOW + relativedelta(months=-1)

        checkout_this_month = CheckOut.objects.filter(checkout_time__month=NOW.month, checkout_time__year=NOW.year)
        total_profit_this_month = checkout_this_month.aggregate(Sum('pay_amount')).get('pay_amount__sum') if checkout_this_month else 0

        checkout_last_month = CheckOut.objects.filter(checkout_time__month=last_month.month, checkout_time__year=last_month.year)
        total_profit_last_month = checkout_last_month.aggregate(Sum('pay_amount')).get('pay_amount__sum') if checkout_last_month else 0

        recurring_profit = []
        this_month_first_period = CheckOut.objects.filter(checkout_time__month=NOW.month, checkout_time__year=NOW.year, checkout_time__day=1)
        profit_first_period_this_month = this_month_first_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if this_month_first_period else 0
        last_month_first_period = CheckOut.objects.filter(checkout_time__month=last_month.month, checkout_time__year=last_month.year, checkout_time__day=1)
        profit_first_period_last_month = last_month_first_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if last_month_first_period else 0
        recurring_profit.append(['Dau thang', profit_first_period_this_month, profit_first_period_last_month])

        for i in range(0, 5):
            this_month_period = CheckOut.objects.filter(checkout_time__month=NOW.month, checkout_time__year=NOW.year, checkout_time__day__gt=i * 5, checkout_time__day__lte=(i+1) * 5)
            profit_period_this_month = this_month_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if this_month_period else 0
            last_month_period = CheckOut.objects.filter(checkout_time__month=last_month.month, checkout_time__year=last_month.year, checkout_time__day__gt=i * 5, checkout_time__day__lte=(i+1) * 5)
            profit_period_last_month = last_month_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if last_month_period else 0
            recurring_profit.append(['Ngay ' + str(i*5) + '-' + str((i+1)*5), profit_period_this_month, profit_period_last_month])

        this_month_last_period = CheckOut.objects.filter(checkout_time__month=NOW.month, checkout_time__year=NOW.year, checkout_time__day__gt=25)
        profit_last_period_this_month = this_month_last_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if this_month_last_period else 0
        last_month_last_period = CheckOut.objects.filter(checkout_time__month=last_month.month, checkout_time__year=last_month.year, checkout_time__day__gt=25)
        profit_last_period_last_month = last_month_last_period.aggregate(Sum('pay_amount')).get('pay_amount__sum') if last_month_last_period else 0
        recurring_profit.append(['Cuoi', profit_last_period_this_month, profit_last_period_last_month])

        profit_growth_month = (total_profit_this_month - total_profit_last_month) / total_profit_last_month * 100 if total_profit_last_month else 0
        target = total_profit_last_month * 105 / 100 if total_profit_last_month > 60000 else 60000
        target_now = total_profit_this_month / target * 100
        month_days = monthrange(NOW.year, NOW.month)
        duration_target = month_days[1] - NOW.day
        duration_target_percent = NOW.day / month_days[1] * 100

        checkin_this_month = CheckIn.objects.filter(checkin_time__month=NOW.month, checkin_time__year=NOW.year).count()
        checkin_last_month = CheckIn.objects.filter(checkin_time__month=last_month.month, checkin_time__year=last_month.year).count()
        checkin_growth_month = (checkin_this_month - checkin_last_month) / checkin_last_month * 100 if checkin_last_month else 0

        booking_this_month_count = Booking.objects.filter(booking_date_time__month=NOW.month, booking_date_time__year=NOW.year).count()
        booking_last_month = Booking.objects.filter(booking_date_time__month=last_month.month, booking_date_time__year=last_month.year).count()
        booking_growth_month = (booking_this_month_count - booking_last_month) / booking_last_month * 100 if booking_last_month else 0
        booking_cancel_this_month = Booking.objects.filter(booking_date_time__month=NOW.month, booking_date_time__year=NOW.year, canceled=True).count()

        bookint_type = BookingType.objects.all()
        booking_type_this_month = dict()
        for bookingtype in bookint_type:
            booking_type_this_month[bookingtype.booking_type] = bookingtype.booking_set.filter(
                booking_date_time__month=NOW.month, booking_date_time__year=NOW.year).count()

        total_room = Room.objects.all().count()
        rooms_available = Room.objects.filter(Q(availability=True) & Q(maintenance=False))
        room_types = RoomType.objects.all()

        room_in_roomtype = dict()
        for roomtype in room_types:
            room_in_roomtype[roomtype.type] = roomtype.room_set.filter(
                Q(availability=True) & Q(maintenance=False)).count()

        new_customers_this_month = Customer.objects.filter(create_at__month=NOW.month, create_at__year=NOW.year).count()
        new_customers_last_month = Customer.objects.filter(create_at__month=last_month.month, create_at__year=last_month.year).count()
        new_customers_growth = (new_customers_this_month - new_customers_last_month) / new_customers_last_month * 100 if new_customers_last_month else 0

        context = super().get_context_data(**kwargs)
        context['today'] = NOW
        context['last_month'] = last_month

        context['total_profit_this_month'] = total_profit_this_month
        context['profit_growth_month'] = profit_growth_month
        context['checkout_this_month'] = checkout_this_month
        context['target'] = target
        context['target_now'] = target_now
        context['duration_target'] = duration_target
        context['duration_target_percent'] = duration_target_percent
        context['recurring_profit'] = recurring_profit

        context['checkin_this_month'] = checkin_this_month
        context['checkin_growth_month'] = checkin_growth_month

        context['booking_type_this_month'] = booking_type_this_month
        context['booking_this_month_count'] = booking_this_month_count
        context['booking_growth_month'] = booking_growth_month
        context['booking_cancel_this_month'] = booking_cancel_this_month
        context['booking_cancel_this_month_percent'] = booking_cancel_this_month / booking_this_month_count * 100 if booking_this_month_count else 0
        context['booking_pending'] = Booking.objects.filter(checkin__isnull=True, canceled=False).count()
        context['reservation_pending'] = Reservation.objects.filter(status='Cho xu ly').count()

        context['total_staff'] = Staff.objects.all().count()
        context['staff_role'] = StaffRole.objects.all()

        context['total_room'] = total_room
        context['rooms_available'] = rooms_available
        context['room_types'] = room_types
        context['room_in_roomtype'] = room_in_roomtype

        context['new_customers_this_month'] = new_customers_this_month
        context['new_customers_growth'] = new_customers_growth
        return context


def loginrequest(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Ten tai khoang va mat khau khong hop le')
    return render(request, 'registration/login.html')


def registeruser(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            pass_word = form.cleaned_data['password1']
            staff_id = form.cleaned_data['staff_id']
            s = get_object_or_404(Staff, staff_id__exact=staff_id)
            s.user = get_object_or_404(User, username__iexact=user_name)
            s.user.set_password(form.cleaned_data['password1'])
            s.user.save()
            s.save()
            Profile.objects.create(user=s.user)
            user_obj = authenticate(request, username=user_name, password=pass_word)
            login(request, user_obj)
            messages.success(request, "Dang ky tai khoan thanh cong", extra_tags='green')
        else:
            messages.error(request, 'Dang ky tai khoan khong thanh cong')
    else:
        form = NewUserForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'registration/userprofile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('userprofile')