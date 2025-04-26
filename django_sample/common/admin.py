from django.contrib import admin

from common.models import Volunteer

# Register your models here.
@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'category', 'is_active', 'priority')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'title', 'bio')
    list_editable = ('priority', 'is_active')