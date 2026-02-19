"""
Content Calendar - Tracks all published content (long-form + shorts).
"""
import json
import re
import uuid
import pickle
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import Counter


CALENDAR_FILE = Path("content_calendar.json")


def _load_data() -> dict:
    if CALENDAR_FILE.exists():
        try:
            with open(CALENDAR_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"entries": []}


def _save_data(data: dict):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _parse_iso8601_duration(duration_str: str) -> int:
    """Parse ISO 8601 duration like PT3M1S → 181 seconds."""
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str or '')
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


# Sync state
_sync_status = {"in_progress": False, "last_result": None, "last_sync": None}


class ContentCalendar:
    """Tracks all published content on a calendar."""

    def add_entry(self, entry: dict):
        data = _load_data()
        if "id" not in entry:
            entry["id"] = str(uuid.uuid4())
        data["entries"].append(entry)
        _save_data(data)
        return entry

    def update_entry(self, entry_id: str, **kwargs):
        data = _load_data()
        for e in data["entries"]:
            if e["id"] == entry_id:
                e.update(kwargs)
                break
        _save_data(data)

    def get_month(self, year: int, month: int) -> list:
        data = _load_data()
        prefix = f"{year}-{month:02d}"
        return [e for e in data["entries"] if e.get("date", "").startswith(prefix)]

    def get_all_entries(self) -> list:
        return _load_data()["entries"]

    def get_stats(self) -> dict:
        data = _load_data()
        entries = data["entries"]
        now = datetime.now()
        today = now.date()
        month_prefix = f"{now.year}-{now.month:02d}"
        week_start = today - timedelta(days=today.weekday())

        published = [e for e in entries if e.get("status") == "published"]
        this_month = [e for e in published if e.get("date", "").startswith(month_prefix)]
        this_week = [
            e for e in published
            if e.get("date") and week_start <= date.fromisoformat(e["date"]) <= today
        ]

        total_views = sum(int(e.get("views", 0)) for e in entries)
        total_likes = sum(int(e.get("likes", 0)) for e in entries)

        # Best performing video
        best = max(entries, key=lambda e: int(e.get("views", 0)), default=None)

        # Domain distribution
        domain_counts = Counter(e.get("domain", "Unknown") for e in published)

        # Consistency: % of last 30 days with content
        days_with_content = set()
        for e in entries:
            d = e.get("date", "")
            if d:
                try:
                    ed = date.fromisoformat(d)
                    if (today - ed).days <= 30:
                        days_with_content.add(d)
                except Exception:
                    pass
        consistency = round(len(days_with_content) / 30 * 100, 1) if entries else 0

        # Weekly breakdown (last 8 weeks)
        weeks = []
        for w in range(8):
            ws = today - timedelta(days=today.weekday() + 7 * w)
            we = ws + timedelta(days=6)
            count = sum(1 for e in published if e.get("date") and ws <= date.fromisoformat(e["date"]) <= we)
            weeks.append({"week_start": ws.isoformat(), "count": count})
        weeks.reverse()

        return {
            "total_published": len(published),
            "total_scheduled": sum(1 for e in entries if e.get("status") == "scheduled"),
            "total_failed": sum(1 for e in entries if e.get("status") == "failed"),
            "total_entries": len(entries),
            "this_month": len(this_month),
            "this_week": len(this_week),
            "total_views": total_views,
            "total_likes": total_likes,
            "best_video": {"title": best.get("title", ""), "views": int(best.get("views", 0)), "youtube_url": best.get("youtube_url", "")} if best else None,
            "by_type": {
                "short": sum(1 for e in entries if e.get("type") == "short"),
                "long": sum(1 for e in entries if e.get("type") == "long"),
            },
            "domain_distribution": dict(domain_counts.most_common(10)),
            "consistency": consistency,
            "weekly_breakdown": weeks,
        }

    async def sync_from_youtube(self) -> dict:
        """Pull ALL videos from YouTube channel and populate calendar."""
        global _sync_status
        _sync_status["in_progress"] = True

        try:
            from domains import DOMAIN_REGISTRY
            domain_names = list(DOMAIN_REGISTRY.keys())

            # Build YouTube service
            token_path = Path("youtube_token.pickle")
            if not token_path.exists():
                _sync_status["in_progress"] = False
                return {"error": "No YouTube token found", "synced": 0, "new": 0, "updated": 0}

            from googleapiclient.discovery import build
            with open(token_path, "rb") as f:
                creds = pickle.load(f)
            youtube = build("youtube", "v3", credentials=creds)

            # Get all video IDs from channel
            all_video_ids = []
            page_token = None
            while True:
                req = youtube.search().list(
                    forMine=True, type="video", maxResults=50,
                    part="id", pageToken=page_token
                )
                resp = req.execute()
                for item in resp.get("items", []):
                    vid = item.get("id", {}).get("videoId")
                    if vid:
                        all_video_ids.append(vid)
                page_token = resp.get("nextPageToken")
                if not page_token:
                    break

            if not all_video_ids:
                _sync_status.update({"in_progress": False, "last_result": {"synced": 0, "new": 0, "updated": 0}, "last_sync": datetime.now().isoformat()})
                return {"synced": 0, "new": 0, "updated": 0}

            # Get details in batches of 50
            data = _load_data()
            existing_yt_ids = {e.get("youtube_id"): e for e in data["entries"] if e.get("youtube_id")}

            new_count = 0
            updated_count = 0

            for i in range(0, len(all_video_ids), 50):
                batch_ids = all_video_ids[i:i+50]
                details_resp = youtube.videos().list(
                    part="snippet,status,contentDetails,statistics",
                    id=",".join(batch_ids)
                ).execute()

                for video in details_resp.get("items", []):
                    vid_id = video["id"]
                    snippet = video.get("snippet", {})
                    status_info = video.get("status", {})
                    content = video.get("contentDetails", {})
                    stats = video.get("statistics", {})

                    # Parse duration
                    duration_s = _parse_iso8601_duration(content.get("duration", ""))
                    vid_type = "short" if duration_s <= 60 else "long"

                    # Parse publish date
                    pub_date_str = snippet.get("publishedAt", "")
                    try:
                        pub_dt = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                        cal_date = pub_dt.strftime("%Y-%m-%d")
                        cal_time = pub_dt.strftime("%I:%M %p")
                    except Exception:
                        cal_date = datetime.now().strftime("%Y-%m-%d")
                        cal_time = ""

                    # Determine status
                    privacy = status_info.get("privacyStatus", "")
                    publish_at = status_info.get("publishAt")
                    if privacy == "public":
                        vid_status = "published"
                    elif publish_at:
                        vid_status = "scheduled"
                        try:
                            sched_dt = datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
                            cal_date = sched_dt.strftime("%Y-%m-%d")
                            cal_time = sched_dt.strftime("%I:%M %p")
                        except Exception:
                            pass
                    else:
                        vid_status = "processing"

                    # Match domain from title using keywords
                    title = snippet.get("title", "")
                    matched_domain = "Unknown"
                    text_lower = (title + " " + snippet.get("description", "")).lower()
                    
                    # Keyword map: domain name → keywords to search for
                    domain_keywords = {
                        "Ancient Places": ["ancient", "ruins", "temple", "pyramid", "fortress"],
                        "Lush Agricultural Farmhouses": ["farm", "agricultural", "harvest", "barn", "crop"],
                        "Ocean & Sea Creatures": ["ocean", "sea", "underwater", "coral", "marine", "dolphin"],
                        "Lush Green Forests": ["forest", "woodland", "green forest", "canopy", "lush green"],
                        "Beautiful Himalayas": ["himalaya", "glacial", "sherpa", "everest", "mountain village"],
                        "Lakeside Lifestyle": ["lake", "lakeside", "pond", "dock"],
                        "Antarctica Beauty": ["antarctic", "iceberg", "penguin", "polar", "glacier"],
                        "Life in Space": ["space", "cosmic", "nebula", "astronaut", "galaxy", "deep space"],
                        "Luxury Cruise Ships": ["cruise", "yacht", "ship", "deck", "marina"],
                        "Desert Life Worldwide": ["desert", "sahara", "dune", "oasis", "arid"],
                        "Tropical Greenery": ["tropical", "palm", "jungle", "exotic", "paradise"],
                        "Buddhist Lifestyle": ["buddhist", "monk", "meditation temple", "zen garden", "dharma"],
                        "Ancient European Cities": ["european", "gothic", "medieval", "cobblestone", "cathedral"],
                        "Japanese Beauty": ["japan", "cherry blossom", "zen", "torii", "kimono", "japanese"],
                        "Amazon Rainforest": ["amazon", "rainforest", "tribal"],
                        "Beautiful Beaches": ["beach", "coastal", "shore", "surf", "seaside"],
                        "Luxury Palace Interiors": ["palace", "mansion", "luxury living", "chandelier", "opulent", "luxury interior"],
                        "Rainy Cozy Interiors": ["rain", "cozy", "fireplace", "book nook"],
                        "Northern Lights & Aurora": ["aurora", "northern light"],
                        "Alpine Villages": ["alpine", "swiss", "chalet", "bavarian"],
                        "Waterfalls & Rivers": ["waterfall", "river", "cascade", "stream"],
                        "Wildlife in Nature": ["wildlife", "deer", "elephant", "bird", "fox"],
                        "Café & Bookshop Ambience": ["cafe", "café", "bookshop", "coffee", "library"],
                    }
                    
                    best_match = "Unknown"
                    best_score = 0
                    for dn, keywords in domain_keywords.items():
                        if dn not in domain_names:
                            continue
                        score = sum(1 for kw in keywords if kw in text_lower)
                        if score > best_score:
                            best_score = score
                            best_match = dn
                    
                    # Also try exact domain name match
                    if best_score == 0:
                        for dn in domain_names:
                            if dn.lower() in text_lower:
                                best_match = dn
                                break
                    
                    matched_domain = best_match

                    entry_data = {
                        "date": cal_date,
                        "time": cal_time,
                        "type": vid_type,
                        "domain": matched_domain,
                        "title": title,
                        "status": vid_status,
                        "youtube_url": f"https://youtube.com/watch?v={vid_id}",
                        "youtube_id": vid_id,
                        "views": int(stats.get("viewCount", 0)),
                        "likes": int(stats.get("likeCount", 0)),
                        "duration": duration_s,
                        "thumbnail_url": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                    }

                    if vid_id in existing_yt_ids:
                        # Update existing
                        existing = existing_yt_ids[vid_id]
                        existing.update(entry_data)
                        existing["id"] = existing.get("id", str(uuid.uuid4()))
                        updated_count += 1
                    else:
                        # New entry
                        entry_data["id"] = str(uuid.uuid4())
                        data["entries"].append(entry_data)
                        new_count += 1

            _save_data(data)
            result = {"synced": len(all_video_ids), "new": new_count, "updated": updated_count}
            _sync_status.update({"in_progress": False, "last_result": result, "last_sync": datetime.now().isoformat()})
            return result

        except Exception as e:
            _sync_status["in_progress"] = False
            print(f"[CALENDAR] Sync error: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e), "synced": 0, "new": 0, "updated": 0}

    @staticmethod
    def get_sync_status() -> dict:
        return _sync_status
