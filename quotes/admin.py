from django.contrib import admin

from .models import Source, Quote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type")
    search_fields = ("name", "type")
    list_filter = ("type",)
    ordering = ("name",)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id", "short_text", "source", "weight", "likes", "dislikes", "views", "created_at")
    list_select_related = ("source",)
    search_fields = ("text", "source__name")
    list_filter = ("source",)
    ordering = ("-created_at",)

    def short_text(self, obj):
        return (obj.text or "")[:70]
    short_text.short_description = "text"
