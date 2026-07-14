from django.contrib import admin

from .models import Course, Video


admin.site.site_header = "lectureLib"
admin.site.site_title = "lectureLib"
admin.site.index_title = "Управление курсами"


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = (
        "position",
        "title",
        "duration_label",
        "bunny_embed_url",
        "is_published",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "code", "instructor", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "code", "instructor")
    inlines = [VideoInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "position",
        "duration_label",
        "is_published",
    )
    list_filter = ("course", "is_published")
    search_fields = ("title", "description", "course__title")
