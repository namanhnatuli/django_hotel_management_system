from rest_framework import serializers

from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["id", "customer_name", "customer_dob", "customer_adress", "customer_phone", "customer_email", "create_at"]
