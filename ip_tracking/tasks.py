from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def flag_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # 1️⃣ Flag IPs exceeding 100 requests/hour
    request_counts = (
        RequestLog.objects
        .filter(created_at__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('id'))
        .filter(count__gt=100)
    )

    for entry in request_counts:
        ip = entry['ip_address']
        count = entry['count']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f'Over 100 requests in last hour ({count})'}
        )

    # 2️⃣ Flag IPs accessing sensitive paths
    sensitive_access = RequestLog.objects.filter(
        created_at__gte=one_hour_ago,
        path__in=SENSITIVE_PATHS
    ).values('ip_address').distinct()

    for entry in sensitive_access:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f'Accessed sensitive path in the last hour'}
        )

