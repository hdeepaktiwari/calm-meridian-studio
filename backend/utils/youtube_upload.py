"""YouTube video upload utility using resumable uploads."""
import pickle
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = Path(__file__).parent.parent / 'youtube_token.pickle'


def _get_youtube_service():
    """Build authenticated YouTube service, refreshing token if needed."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(
            "YouTube token not found. Run youtube_auth.py first."
        )

    with open(TOKEN_FILE, 'rb') as f:
        credentials = pickle.load(f)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(credentials, f)

    return build('youtube', 'v3', credentials=credentials)


def _get_scheduled_slots(youtube) -> set:
    """Fetch all already-scheduled publish dates (as IST date strings) from YouTube."""
    ist = ZoneInfo("Asia/Kolkata")
    taken = set()
    try:
        # Get all private videos (scheduled videos are private with publishAt)
        request = youtube.videos().list(
            part='status',
            mine=True,
            maxResults=50,
        )
        # Use search instead — videos().list with mine=True needs different approach
        request = youtube.search().list(
            part='snippet',
            forMine=True,
            type='video',
            maxResults=50,
        )
        response = request.execute()
        video_ids = [item['id']['videoId'] for item in response.get('items', [])]

        if video_ids:
            # Fetch status for these videos
            details = youtube.videos().list(
                part='status',
                id=','.join(video_ids),
            ).execute()

            for item in details.get('items', []):
                publish_at = item.get('status', {}).get('publishAt')
                if publish_at:
                    # Parse and convert to IST date
                    dt = datetime.fromisoformat(publish_at.replace('Z', '+00:00'))
                    dt_ist = dt.astimezone(ist)
                    taken.add(dt_ist.strftime("%Y-%m-%d"))
    except Exception as e:
        print(f"⚠️ Could not fetch scheduled slots: {e}")

    return taken


def _get_next_publish_time(youtube=None) -> str:
    """Get the next available 8:00 AM IST slot not already taken by a scheduled video."""
    ist = ZoneInfo("Asia/Kolkata")
    now_ist = datetime.now(ist)

    # Get already-taken slots
    taken_dates = set()
    if youtube:
        taken_dates = _get_scheduled_slots(youtube)
        if taken_dates:
            print(f"📋 Already scheduled dates: {sorted(taken_dates)}")

    # Start from next 8 AM IST
    target = now_ist.replace(hour=8, minute=0, second=0, microsecond=0)
    if now_ist >= target - timedelta(minutes=10):
        target += timedelta(days=1)

    # Find next available slot
    while target.strftime("%Y-%m-%d") in taken_dates:
        target += timedelta(days=1)

    target_utc = target.astimezone(ZoneInfo("UTC"))
    return target_utc.strftime("%Y-%m-%dT%H:%M:%S.0Z")


def upload_video(
    video_path: str,
    title: str,
    description: str,
    tags: list[str],
    category_id: str = '22',
    privacy: str = 'private',
    thumbnail_path: Optional[str] = None,
    schedule: bool = True,
) -> dict:
    """Upload video to YouTube with resumable upload.

    If schedule=True (default) and privacy is public/unlisted,
    auto-schedules to go public at 8:00 AM IST (next occurrence).

    Returns: { video_id, url, scheduled_at }
    """
    youtube = _get_youtube_service()

    status_body = {
        'privacyStatus': privacy,
        'selfDeclaredMadeForKids': False,
    }

    scheduled_at = None
    if schedule and privacy in ('public', 'unlisted'):
        scheduled_at = _get_next_publish_time(youtube)
        status_body['privacyStatus'] = 'private'
        status_body['publishAt'] = scheduled_at
        ist_time = datetime.fromisoformat(scheduled_at.replace('.0Z', '+00:00')).astimezone(ZoneInfo("Asia/Kolkata"))
        print(f"📅 Scheduled to go public: {ist_time.strftime('%A, %d %b %Y at %I:%M %p IST')}")

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id,
        },
        'status': status_body,
    }

    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True, chunksize=10 * 1024 * 1024)

    request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()

    video_id = response['id']

    if thumbnail_path and Path(thumbnail_path).exists():
        set_thumbnail(video_id, thumbnail_path, youtube)

    result = {
        'video_id': video_id,
        'url': f'https://www.youtube.com/watch?v={video_id}',
    }
    if scheduled_at:
        result['scheduled_at'] = scheduled_at
    return result


def set_thumbnail(video_id: str, thumbnail_path: str, youtube=None):
    """Set custom thumbnail for a video."""
    if youtube is None:
        youtube = _get_youtube_service()

    media = MediaFileUpload(thumbnail_path, mimetype='image/jpeg')
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
