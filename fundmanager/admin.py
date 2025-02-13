from django.contrib import admin
from .models import Event, Branch, Payment

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'admission_number', 'department', 'batch') #To show the added field in the userlist in admin
    def admission_number(self, obj):
        return obj.profile.admission_number
    admission_number.short_description = 'Admission Number'

    def department(self, obj):
        return obj.profile.department
    department.short_description = 'Department'

    def batch(self, obj):
        return obj.profile.batch
    batch.short_description = 'Batch'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Payment)
admin.site.register(Branch)
admin.site.register(Event)