from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BunnyVideoData:
    guid: str
    title: str
    description: str
    length: int | None
    thumbnail_url: str
    player_embed_url: str
    api_error: str = ""


class BunnyAPIError(Exception):
    pass


def _player_embed_url(video_id: str) -> str:
    return (
        f"https://iframe.mediadelivery.net/embed/"
        f"{settings.BUNNY_STREAM_LIBRARY_ID}/{video_id}"
        "?autoplay=false&loop=false&muted=false&preload=true&responsive=true"
    )


def _duration_label(seconds: int | None) -> str:
    if not seconds:
        return ""
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"


def _fetch_video(video_id: str) -> dict:
    access_key = settings.BUNNY_STREAM_API_KEY
    if not access_key:
        raise BunnyAPIError(
            "Bunny API key is not configured. Set BUNNY_STREAM_API_KEY "
            "or BUNNY_API_KEY on the Railway web service."
        )

    url = (
        f"https://video.bunnycdn.com/library/"
        f"{settings.BUNNY_STREAM_LIBRARY_ID}/videos/{video_id}"
    )
    request = Request(
        url,
        headers={
            "AccessKey": access_key,
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=settings.BUNNY_STREAM_API_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise BunnyAPIError(f"Bunny API returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise BunnyAPIError(f"Bunny API request failed: {exc.reason}") from exc
    except (TimeoutError, json.JSONDecodeError) as exc:
        raise BunnyAPIError("Bunny API response could not be read") from exc


def get_video_data(video_id: str) -> BunnyVideoData:
    api_error = ""
    payload = {}
    try:
        payload = _fetch_video(video_id)
    except BunnyAPIError as exc:
        api_error = str(exc)
        logger.warning("Could not fetch Bunny video %s: %s", video_id, exc)

    guid = payload.get("guid") or video_id
    title = payload.get("title") or f"Видео {video_id}"
    description = payload.get("description") or "Описание видео будет получено из Bunny Stream."
    length = payload.get("length")
    thumbnail_url = payload.get("thumbnailUrl") or ""

    if length is not None:
        description = f"{description}\n\nДлительность: {_duration_label(length)}"

    return BunnyVideoData(
        guid=guid,
        title=title,
        description=description,
        length=length,
        thumbnail_url=thumbnail_url,
        player_embed_url=_player_embed_url(guid),
        api_error=api_error,
    )
