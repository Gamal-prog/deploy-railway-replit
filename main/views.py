from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Course, Video
from .services.bunny import get_video_data


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")


def course_list(request):
    courses = Course.objects.annotate(video_count=Count("videos")).order_by("name")
    total_videos = sum(course.video_count for course in courses)
    return render(
        request,
        "main/course_list.html",
        {
            "courses": courses,
            "total_videos": total_videos,
        },
    )


def _lecture_payload(video: Video) -> dict:
    bunny_video = get_video_data(video.bunny_video_id)
    return {
        "id": video.id,
        "name": bunny_video.title,
        "description": bunny_video.description,
        "player_embed_url": bunny_video.player_embed_url,
        "thumbnail_url": bunny_video.thumbnail_url,
        "api_error": bunny_video.api_error,
    }


def course_player(request, course_pk, video_pk=None):
    course = get_object_or_404(Course, pk=course_pk)
    videos = list(course.videos.order_by("id"))

    selected_video = None
    if video_pk is not None:
        selected_video = get_object_or_404(Video, pk=video_pk, course=course)
    elif videos:
        selected_video = videos[0]

    lectures = [_lecture_payload(video) for video in videos]
    initial_lecture = None
    if selected_video is not None:
        initial_lecture = next(
            (lecture for lecture in lectures if lecture["id"] == selected_video.id),
            lectures[0] if lectures else None,
        )

    return render(
        request,
        "main/lecture.html",
        {
            "course": course,
            "album_lectures": {"data": lectures},
            "initial_lecture": initial_lecture,
            "bunny_api_error": next(
                (lecture["api_error"] for lecture in lectures if lecture["api_error"]),
                "",
            ),
        },
    )
