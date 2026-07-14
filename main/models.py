from django.db import models


class Course(models.Model):
    title = models.CharField("Название", max_length=180)
    code = models.CharField("Код курса", max_length=32, blank=True)
    summary = models.CharField("Краткое описание", max_length=260, blank=True)
    description = models.TextField("Описание", blank=True)
    instructor = models.CharField("Преподаватель", max_length=120, blank=True)
    cover_url = models.URLField("Обложка", blank=True)
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.title

    @property
    def published_videos(self):
        return self.videos.filter(is_published=True)


class Video(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        related_name="videos",
        on_delete=models.CASCADE,
    )
    title = models.CharField("Название", max_length=180)
    description = models.TextField("Описание", blank=True)
    bunny_embed_url = models.URLField(
        "Bunny embed URL",
        help_text="Например: https://iframe.mediadelivery.net/embed/...",
    )
    duration_label = models.CharField("Длительность", max_length=32, blank=True)
    position = models.PositiveIntegerField("Порядок", default=1)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "видео"
        verbose_name_plural = "видео"

    def __str__(self):
        return f"{self.course}: {self.title}"
