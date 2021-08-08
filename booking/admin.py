from django.contrib import admin
from booking.models import CheckIn, Service, CheckOut, Booking, BookingType

# Register your models here.

admin.site.register(CheckIn)
admin.site.register(Service)
admin.site.register(CheckOut)
admin.site.register(BookingType)


@admin.register(Booking)
class BookkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'canceled', 'booking_date_time')

