from django.conf import settings


def branding(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Цитаткин"),
        "SITE_LOGO": getattr(settings, "SITE_LOGO", "branding/logo.svg"),
    }
