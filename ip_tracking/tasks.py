from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def flag_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # 1️⃣ IPs exceeding 100 requests/hour
    logs = RequestLog.objects.filter(created_at__gte=one_hour_ago)
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f'Over 100 requests in last hour ({count})'}
            )

    # 2️⃣ IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login']
    sensitive_logs = logs.filter(path__in=sensitive_paths)
    for log in sensitive_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log.ip_address,
            defaults={'reason': f'Accessed sensitive path: {log.path}'}
        )

