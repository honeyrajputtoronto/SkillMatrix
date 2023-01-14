from django.contrib import admin
from .models import RegisterHustler, RegisterRecruiter
from django.contrib.auth.models import Group

# admin.register() decorator
@admin.register(RegisterHustler)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'university', 'skills']

# admin.register() decorator
@admin.register(RegisterRecruiter)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'company_name', 'skills']

admin.site.unregister(Group)

admin.site.site_header = 'Product Review Admin'

