from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
import ipapi
from django.core.cache import cache

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip_address = self.get_client_ip(request)

        # Block if blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Get geolocation, cache for 24 hours
        cache_key = f"geo_{ip_address}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            try:
                geo = ipapi.location(ip=ip_address)
                geo_data = {"country": geo.get("country_name"), "city": geo.get("city")}
            except Exception:
                geo_data = {"country": "Unknown", "city": "Unknown"}
            cache.set(cache_key, geo_data, 24*60*60)  # 24 hours

        country = geo_data.get("country", "Unknown")
        city = geo_data.get("city", "Unknown")

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            country=country,
            city=city
        )

        # Continue to view
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

