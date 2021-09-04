from rest_framework import serializers

from booking.models import Service, BookingType, Booking, CheckIn, CheckOut


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ["service_type", "service_price"]


class BookingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingType
        fields = ["booking_type"]


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['id', 'booking_type', 'customer', 'user', 'no_of_adults', 'no_of_children', 'booking_date_time', 'arrival_date_time', 'departure_date_time', 'description', 'updated_at', 'canceled']
        read_only_fields = ['booking_date_time', 'user']


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = ['booking', 'rooms', 'services', 'departure_date_time', 'user',
                  'checkin_time', 'initial_amount', 'updated_at']
        read_only_fields = ['user']


class CheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckOut
        fields = ['checkin', 'checkout_time', 'stay_duration', 'total_amount', 'pay_amount',
                  'extra_fee', 'discount', 'vat', 'payment_type', 'checkout_by']
        read_only_fields = ['checkout_by']


