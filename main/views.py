from django.http import HttpResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Course, Video


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")


def course_list(request):
    courses = (
        Course.objects.filter(is_published=True)
        .annotate(
            published_video_count=Count(
                "videos",
                filter=Q(videos__is_published=True),
            )
        )
        .prefetch_related("videos")
        .order_by("title")
    )
    return render(request, "main/course_list.html", {"courses": courses})


def course_detail(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, is_published=True)
    videos = course.published_videos
    featured_video = videos.first()
    return render(
        request,
        "main/course_detail.html",
        {
            "course": course,
            "videos": videos,
            "featured_video": featured_video,
        },
    )


def video_player(request, course_pk, video_pk):
    course = get_object_or_404(Course, pk=course_pk, is_published=True)
    videos = course.published_videos
    video = get_object_or_404(Video, pk=video_pk, course=course, is_published=True)
    return render(
        request,
        "main/video_player.html",
        {
            "course": course,
            "video": video,
            "videos": videos,
        },
    )
