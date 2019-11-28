from django.contrib import admin
from .models import *


class VariantOptionGuardInline(admin.TabularInline):
    model = VariantOptionGuard
    extra = 1


class OptionGuardAdmin(admin.ModelAdmin):
    inlines = [VariantOptionGuardInline, ]


admin.site.register(OptionGuard, OptionGuardAdmin)
admin.site.register(Job, )
admin.site.register(GuardFirm, )
admin.site.register(Role, )
admin.site.register(UserProfile, )
