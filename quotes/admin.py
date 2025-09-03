from django.contrib import admin
from .models import Source, Quote
from django.conf import settings


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name", "type")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "source", "weight", "likes", "dislikes", "views")
    list_filter = ("source",)
    search_fields = ("text",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        if len(obj.text) > 60:
            return f"{obj.text[:60]}…"
        return obj.text


admin.site.site_header = f"{settings.SITE_NAME} — админка"
admin.site.site_title = settings.SITE_NAME
admin.site.index_title = "Управление контентом"
