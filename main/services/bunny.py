from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from urllib.parse import urlencode
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
    query = {
        "autoplay": "true",
        "loop": "false",
        "muted": "true",
        "preload": "true",
        "responsive": "true",
    }

    token_key = getattr(settings, "BUNNY_STREAM_EMBED_TOKEN_KEY", "")
    if token_key:
        expires = int(time.time()) + settings.BUNNY_STREAM_EMBED_TOKEN_TTL
        token_source = f"{token_key}{video_id}{expires}".encode("utf-8")
        query["token"] = hashlib.sha256(token_source).hexdigest()
        query["expires"] = str(expires)

    return (
        f"https://player.mediadelivery.net/embed/"
        f"{settings.BUNNY_STREAM_LIBRARY_ID}/{video_id}?{urlencode(query)}"
    )


def _duration_label(seconds: int | None) -> str:
    if not seconds:
        return ""
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"


def _as_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _playback_diagnostics(payload: dict) -> str:
    if not payload:
        return ""

    notes = []
    length = _as_int(payload.get("length"))
    encode_progress = _as_int(payload.get("encodeProgress"))
    available_resolutions = str(payload.get("availableResolutions") or "").strip()
    status = payload.get("status")

    if length is not None and length <= 0:
        notes.append("длительность в Bunny API равна 0")

    if encode_progress is not None and encode_progress < 100:
        notes.append(f"кодирование завершено на {encode_progress}%")

    if not available_resolutions:
        notes.append("нет доступных разрешений")

    if payload.get("isPublic") is False:
        notes.append("видео отмечено как непубличное")

    transcoding_messages = payload.get("transcodingMessages") or []
    if transcoding_messages:
        last_message = transcoding_messages[-1] or {}
        message = last_message.get("message") or last_message.get("issueCode")
        if message:
            notes.append(f"последнее сообщение транскодинга: {message}")

    if not notes:
        return ""

    facts = [
        f"status={status}",
        f"encodeProgress={encode_progress if encode_progress is not None else 'unknown'}",
        f"availableResolutions={available_resolutions or 'none'}",
    ]
    return "\n\nДиагностика Bunny: " + "; ".join(notes) + ". (" + ", ".join(facts) + ")"


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
    duration = _duration_label(length)

    if duration:
        description = f"{description}\n\nДлительность: {duration}"

    description = f"{description}{_playback_diagnostics(payload)}"

    return BunnyVideoData(
        guid=guid,
        title=title,
        description=description,
        length=length,
        thumbnail_url=thumbnail_url,
        player_embed_url=_player_embed_url(guid),
        api_error=api_error,
    )
