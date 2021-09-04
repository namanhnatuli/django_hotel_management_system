from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions

from booking.models import Service, BookingType, Booking, CheckIn, CheckOut
from booking.serializers import ServiceSerializer, BookingTypeSerializer, BookingSerializer, CheckInSerializer, \
    CheckOutSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class BookingTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = BookingType.objects.all()
    serializer_class = BookingTypeSerializer


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class CheckInViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer


class CheckOutViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = CheckOut.objects.all()
    serializer_class = CheckOutSerializer
