# Django Middleware for logging requests
import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure the logger
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')  # Log to this file
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour in 24-hour format
        current_hour = datetime.now().hour

        # Allow access only between 18 (6PM) and 21 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the messaging app is only allowed between 6PM and 9PM.")

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}  # Dictionary to track IPs and timestamps

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Only apply rate limit to POST requests to /api/messages/
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            now = datetime.now()

            # Initialize if IP is new
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove timestamps older than 1 minute
            self.ip_requests[ip] = [
                timestamp for timestamp in self.ip_requests[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            if len(self.ip_requests[ip]) >= 5:
                return JsonResponse({
                    'error': 'Rate limit exceeded. Max 5 messages per minute.'
                }, status=429)

            # Record the new request
            self.ip_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handle cases behind proxies/load balancers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check roles for specific paths (e.g., message management)
        protected_paths = ['/api/messages/', '/admin/']  # customize this as needed

        if any(request.path.startswith(p) for p in protected_paths):
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=403)

            # Check if user is admin or moderator
            if not (user.is_superuser or user.groups.filter(name__in=['moderator']).exists()):
                return JsonResponse({'error': 'Access denied: Admin or Moderator only'}, status=403)

        return self.get_response(request)