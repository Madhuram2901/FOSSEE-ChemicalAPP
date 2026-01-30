import logging
from django.http import JsonResponse
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            return JsonResponse({
                "error": "Validation Error",
                "message": exception.message if hasattr(exception, 'message') else str(exception)
            }, status=400)
            
        logger.error(f"Unhandled Exception: {str(exception)}", exc_info=True)
        return JsonResponse({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please contact support."
        }, status=500)
