from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'count', 'created_at')  
    ordering = ('created_at',)  

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'blocked_at')
    ordering = ('blocked_at',)

@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'flagged_at')
    ordering = ('flagged_at',)

