from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from .models import UserProfile

class LanguagePreferenceMiddleware(MiddlewareMixin):
    """
    Middleware that sets the user's preferred language from their profile.
    This runs after Django's LocaleMiddleware to override the language
    based on user preference.
    """

    def process_request(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                if user_profile.language_preference:
                    translation.activate(user_profile.language_preference)
                    request.LANGUAGE_CODE = user_profile.language_preference
            except UserProfile.DoesNotExist:
                pass