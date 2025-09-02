from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

# Login view with rate limiting
# 10 requests/minute for authenticated users (POST)
# 5 requests/minute for anonymous users (GET)
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def login_view(request):
    # If request is blocked by rate limit
    if getattr(request, 'limited', False):
        return HttpResponse("Too many requests. Try again later.", status=429)

    # Example login logic (replace with your real login code)
    if request.method == "POST":
        return HttpResponse("Processing login...")
    else:
        return HttpResponse("Login page")

