from django.contrib import admin
from staff.models import Staff, StaffRole
# Register your models here.

# admin.site.register(Staff)
admin.site.register(StaffRole)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    # To show in admin app
    list_display = (
        'staff_id',
        'last_name',
        'first_name',
        'staff_role',
        'staff_email',
        'user',
    )