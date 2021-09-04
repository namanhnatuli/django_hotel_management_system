from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly

from room.serializers import RoomSerializer, RoomTypeSerializer, FacilitySerializer
from room.models import Room, RoomType, Facility


class FacilityViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()


class RoomTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


