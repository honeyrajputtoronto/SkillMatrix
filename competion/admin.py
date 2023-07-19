from django.contrib import admin
from .models import Competition
# Register your models here.
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['competition_id','competition','time','room_time']
    exclude = ['level','left_level']


admin.site.register(Competition,CompetitionAdmin)
