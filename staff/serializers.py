from rest_framework import serializers

from staff.models import StaffRole, Staff


class StaffRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffRole
        fields = ["role"]


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ["staff_id", "first_name", "last_name", "staff_role", "staff_email", "user"]
        read_only_fields = ['user']
