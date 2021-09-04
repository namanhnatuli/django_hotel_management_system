from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from staff.models import Staff, StaffRole
from staff.serializers import StaffSerializer, StaffRoleSerializer


class StaffRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer


class StaffViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


