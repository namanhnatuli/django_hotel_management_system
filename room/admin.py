from django.contrib import admin
from room.models import Room, RoomType, Facility
# Register your models here.

# admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Facility)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'availability', 'maintenance')

