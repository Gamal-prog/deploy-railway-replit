from django.db import migrations, models


def copy_bunny_video_id_from_embed_url(apps, schema_editor):
    Video = apps.get_model("main", "Video")
    for video in Video.objects.all():
        embed_url = getattr(video, "bunny_embed_url", "") or ""
        bunny_video_id = ""
        if "/embed/" in embed_url:
            parts = [part for part in embed_url.split("?")[0].split("/") if part]
            if parts:
                bunny_video_id = parts[-1]
        video.bunny_video_id = bunny_video_id
        video.save(update_fields=["bunny_video_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_mvp_course_video"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="title",
            new_name="name",
        ),
        migrations.AddField(
            model_name="video",
            name="bunny_video_id",
            field=models.CharField(blank=True, default="", max_length=80, verbose_name="Bunny video ID"),
        ),
        migrations.RunPython(copy_bunny_video_id_from_embed_url, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="course",
            name="code",
        ),
        migrations.RemoveField(
            model_name="course",
            name="cover_url",
        ),
        migrations.RemoveField(
            model_name="course",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="course",
            name="description",
        ),
        migrations.RemoveField(
            model_name="course",
            name="instructor",
        ),
        migrations.RemoveField(
            model_name="course",
            name="is_published",
        ),
        migrations.RemoveField(
            model_name="course",
            name="summary",
        ),
        migrations.RemoveField(
            model_name="course",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="video",
            name="bunny_embed_url",
        ),
        migrations.RemoveField(
            model_name="video",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="video",
            name="description",
        ),
        migrations.RemoveField(
            model_name="video",
            name="duration_label",
        ),
        migrations.RemoveField(
            model_name="video",
            name="is_published",
        ),
        migrations.RemoveField(
            model_name="video",
            name="position",
        ),
        migrations.RemoveField(
            model_name="video",
            name="title",
        ),
        migrations.RemoveField(
            model_name="video",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="video",
            name="bunny_video_id",
            field=models.CharField(max_length=80, verbose_name="Bunny video ID"),
        ),
        migrations.AlterModelOptions(
            name="course",
            options={"ordering": ["name"], "verbose_name": "курс", "verbose_name_plural": "курсы"},
        ),
        migrations.AlterModelOptions(
            name="video",
            options={"ordering": ["id"], "verbose_name": "видео", "verbose_name_plural": "видео"},
        ),
    ]
