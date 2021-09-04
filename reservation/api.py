from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, AllowAny, IsAdminUser

from reservation.models import Reservation
from reservation.serializers import BookingSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Reservation.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            permission_classes = [DjangoModelPermissions]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
