from django.db import models


class Course(models.Model):
    name = models.CharField("Название", max_length=180)

    class Meta:
        ordering = ["name"]
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.name


class Video(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        related_name="videos",
        on_delete=models.CASCADE,
    )
    bunny_video_id = models.CharField("Bunny video ID", max_length=80)

    class Meta:
        ordering = ["id"]
        verbose_name = "видео"
        verbose_name_plural = "видео"

    def __str__(self):
        return f"{self.course}: {self.bunny_video_id}"
