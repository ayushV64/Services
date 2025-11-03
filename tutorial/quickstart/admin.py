from django.contrib import admin
from . import models
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(models.student)
admin.site.register(models.Book)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(models.studentDetails)
class studentDetail(admin.ModelAdmin):
    list_display = ['student', 'address', 'phoneNumber']
    list_display_links = ['student', 'address', 'phoneNumber']