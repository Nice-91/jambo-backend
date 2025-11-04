from django.contrib import admin
from .models import User, Device

# -----------------------------
# Custom User Admin
# -----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined',)

# -----------------------------
# Device Admin
# -----------------------------
@admin.action(description="Mark selected devices as verified")
def verify_devices(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_id', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__email', 'device_id')
    readonly_fields = ('id',)
    actions = [verify_devices]
