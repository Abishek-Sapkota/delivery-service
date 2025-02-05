from threading import local

# from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()


def get_current_request():
    """
    :returns the HttpRequest object for this thread
    """
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """
    :returns the current user if it exists or None otherwise
    """
    request = get_current_request()
    if request:
        return getattr(request, "user", None)


class ThreadLocalMiddleware(object):
    """
    Middleware to add the HttpRequest to thread local storage
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        return self.get_response(request)

# class TimezoneMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         from apps.configuration.models import BasicWebsiteConfiguration
#         try:
#             config = BasicWebsiteConfiguration.objects.first()
#             if config:
#                 tz = config.timezone
#             else:
#                 from pytz import timezone
#                 tz = timezone('UTC')
#         except BasicWebsiteConfiguration.DoesNotExist as e:
#             from pytz import timezone
#             tz = timezone('UTC')
#         import django.utils.timezone
#         if tz:
#             django.utils.timezone.activate(tz)
#         else:
#             django.utils.timezone.deactivate()
