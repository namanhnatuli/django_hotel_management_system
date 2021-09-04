from rest_framework import serializers

from reservation.models import Reservation


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'guest_name', 'guest_phone', 'guest_email', 'no_of_adults', 'no_of_children', 'reservation_date_time', 'expected_arrival_date_time', 'expected_departure_date_time', 'status', 'user', 'updated_at']
        read_only_fields = ['reservation_date_time', 'user', 'updated_at']
