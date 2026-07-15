from django.contrib import admin

from .models import Course, Video


admin.site.site_header = "lectureLib"
admin.site.site_title = "lectureLib"
admin.site.index_title = "Управление курсами"


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ("bunny_video_id",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "video_count")
    search_fields = ("name",)
    inlines = [VideoInline]

    @admin.display(description="Видео")
    def video_count(self, obj):
        return obj.videos.count()


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "bunny_video_id")
    list_filter = ("course",)
    search_fields = ("bunny_video_id", "course__name")
