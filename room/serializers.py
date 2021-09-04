from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from room.models import Room, RoomType, Facility


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['facility_type']


class RoomTypeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super(RoomTypeSerializer, self).to_representation(instance)
        rep['facility'] = [facility.facility_type for facility in instance.facility.all()]
        return rep

    class Meta:
        model = RoomType
        fields = ['id', 'type', 'facility', 'description', 'price']


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'maintenance', 'availability', 'url']

    def to_representation(self, instance):
        rep = super(RoomSerializer, self).to_representation(instance)
        rep['room_type'] = instance.room_type.type
        return rep


