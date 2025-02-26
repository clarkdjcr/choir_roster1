from django.contrib import admin
from .models import ChoirMember, Attendance, Performance

@admin.register(ChoirMember)
class ChoirMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'voice_part', 'folder_number', 'active', 'join_date')
    list_filter = ('voice_part', 'active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'date', 'will_attend')
    list_filter = ('date', 'will_attend')
    search_fields = ('member__user__username',)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('song_title', 'date')
    search_fields = ('song_title',)
# Register your models here.
