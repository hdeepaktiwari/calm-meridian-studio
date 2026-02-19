"""
Content Calendar - Tracks all published content (long-form + shorts).
"""
import json
import uuid
from pathlib import Path
from datetime import datetime, date, timedelta


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

        return {
            "total_published": len(published),
            "total_scheduled": sum(1 for e in entries if e.get("status") == "scheduled"),
            "total_failed": sum(1 for e in entries if e.get("status") == "failed"),
            "this_month": len(this_month),
            "this_week": len(this_week),
            "by_type": {
                "short": sum(1 for e in published if e.get("type") == "short"),
                "long": sum(1 for e in published if e.get("type") == "long"),
            },
        }
