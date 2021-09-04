from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from customer.models import Customer
from customer.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
