"""
CEO Agent — Chief Executive Officer for Calm Meridian autonomous operations.
Monitors all systems and takes corrective action when needed.
"""
import json
import shutil
import os
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
LOG_FILE = Path("ceo_log.json")
MAX_LOG_ENTRIES = 100


def _load_log() -> list:
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_log(entries: list):
    with open(LOG_FILE, "w") as f:
        json.dump(entries[-MAX_LOG_ENTRIES:], f, indent=2, default=str)


class CEOAgent:
    """Chief Executive Officer Agent — oversees all Calm Meridian operations."""

    async def run_health_check(self) -> dict:
        report = {
            "timestamp": datetime.now(IST).isoformat(),
            "checks": {},
            "actions_taken": [],
            "alerts": [],
            "overall_status": "healthy",
        }

        await self._check_idea_bank(report)
        await self._check_shorts_publisher(report)
        await self._check_longform_pipeline(report)
        await self._check_comment_responder(report)
        await self._check_youtube_token(report)
        await self._check_disk_space(report)
        await self._check_failed_jobs(report)

        # Determine overall status
        if report["alerts"]:
            report["overall_status"] = "critical"
        elif any(
            c.get("status") == "warning"
            for c in report["checks"].values()
        ):
            report["overall_status"] = "degraded"

        self._log_report(report)
        return report

    async def _check_idea_bank(self, report):
        try:
            from ideas.idea_bank import IdeaBank
            bank = IdeaBank()
            stats = bank.get_stats()
            available = stats.get("available", 0)

            check = {
                "status": "healthy",
                "available": available,
                "total": stats.get("total", 0),
            }

            if available < 20:
                check["status"] = "warning"
                if available < 10:
                    check["status"] = "critical"
                # Auto-generate ideas
                try:
                    print("[CEO] Idea bank low, generating 100 ideas...")
                    await bank.generate_ideas(100)
                    report["actions_taken"].append(
                        f"Auto-generated 100 ideas (was {available} available)"
                    )
                    check["action"] = "generated_100"
                except Exception as e:
                    report["alerts"].append(
                        f"Failed to auto-generate ideas: {e}"
                    )

            report["checks"]["idea_bank"] = check
        except Exception as e:
            report["checks"]["idea_bank"] = {"status": "error", "error": str(e)}

    async def _check_shorts_publisher(self, report):
        try:
            from ideas.auto_publisher import AutoPublisher, _load_state
            state = _load_state()
            enabled = state.get("enabled", False)
            check = {
                "status": "healthy" if enabled else "warning",
                "enabled": enabled,
                "recent_slots": len(state.get("published_slots", [])),
            }
            if not enabled:
                check["note"] = "Shorts auto-publisher is disabled"
            report["checks"]["shorts_publisher"] = check
        except Exception as e:
            report["checks"]["shorts_publisher"] = {"status": "error", "error": str(e)}

    async def _check_longform_pipeline(self, report):
        try:
            from ideas.long_form_publisher import LongFormPublisher
            pub = LongFormPublisher()
            status = pub.get_status()
            check = {
                "status": "healthy",
                "enabled": status.get("enabled", False),
                "days_of_buffer": status.get("days_of_buffer") or 0,
                "last_generated": status.get("last_generated"),
            }
            if not status.get("enabled", False):
                check["status"] = "warning"
                check["note"] = "Long-form auto-publisher is disabled"
                # Auto-enable
                try:
                    pub._save_state({"enabled": True, **pub._load_state()})
                    check["action"] = "auto_enabled"
                    report["actions_taken"].append("Auto-enabled long-form publisher")
                except Exception:
                    pass
            elif (status.get("days_of_buffer") or 0) < 1:
                check["status"] = "warning"
            report["checks"]["longform_pipeline"] = check
        except Exception as e:
            report["checks"]["longform_pipeline"] = {"status": "error", "error": str(e)}

    async def _check_comment_responder(self, report):
        """Verify comment responder is enabled and last check was within 12 hours."""
        try:
            from comments.responder import CommentResponder
            responder = CommentResponder()
            status = responder.get_status()
            check = {
                "status": "healthy",
                "enabled": status.get("enabled", False),
                "total_replies": status.get("total_replies", 0),
                "last_check": status.get("last_check"),
            }
            if not status.get("enabled", False):
                check["status"] = "warning"
                check["note"] = "Comment responder is disabled"
            elif status.get("last_check"):
                last = datetime.fromisoformat(status["last_check"])
                if (datetime.now(IST) - last).total_seconds() > 12 * 60 * 60:
                    check["status"] = "warning"
                    check["note"] = "Last comment check was over 12 hours ago"
            report["checks"]["comment_responder"] = check
        except Exception as e:
            report["checks"]["comment_responder"] = {"status": "error", "error": str(e)}

    async def _check_youtube_token(self, report):
        try:
            token_path = Path("youtube_token.pickle")
            check = {"status": "healthy", "token_exists": token_path.exists()}
            if not token_path.exists():
                check["status"] = "critical"
                report["alerts"].append("YouTube token missing! Run youtube_auth.py")
            else:
                # Try refreshing proactively
                try:
                    import pickle
                    from google.auth.transport.requests import Request
                    with open(token_path, "rb") as f:
                        creds = pickle.load(f)
                    if creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                        with open(token_path, "wb") as f:
                            pickle.dump(creds, f)
                        report["actions_taken"].append("Refreshed YouTube token")
                        check["action"] = "token_refreshed"
                    check["valid"] = creds.valid
                    check["expired"] = creds.expired
                except Exception as e:
                    check["refresh_error"] = str(e)
            report["checks"]["youtube_token"] = check
        except Exception as e:
            report["checks"]["youtube_token"] = {"status": "error", "error": str(e)}

    async def _check_disk_space(self, report):
        try:
            usage = shutil.disk_usage("/")
            free_gb = usage.free / (1024**3)
            check = {
                "status": "healthy",
                "free_gb": round(free_gb, 1),
                "total_gb": round(usage.total / (1024**3), 1),
            }
            if free_gb < 5:
                check["status"] = "warning"
            if free_gb < 2:
                check["status"] = "critical"
                report["alerts"].append(f"Disk space critically low: {free_gb:.1f} GB free")
            report["checks"]["disk_space"] = check
        except Exception as e:
            report["checks"]["disk_space"] = {"status": "error", "error": str(e)}

    async def _check_failed_jobs(self, report):
        try:
            from main import jobs
            failed = [j for j in jobs.values() if j.get("status") == "failed"]
            stuck = [
                j for j in jobs.values()
                if j.get("status") == "running"
                and j.get("created_at")
                and (datetime.now() - datetime.fromisoformat(j["created_at"])).total_seconds() > 3600
            ]
            check = {
                "status": "healthy",
                "failed_count": len(failed),
                "stuck_count": len(stuck),
            }
            if failed or stuck:
                check["status"] = "warning"
            if len(failed) > 5 or len(stuck) > 2:
                check["status"] = "critical"
                report["alerts"].append(
                    f"{len(failed)} failed jobs, {len(stuck)} stuck jobs"
                )
            report["checks"]["failed_jobs"] = check
        except Exception as e:
            report["checks"]["failed_jobs"] = {"status": "error", "error": str(e)}

    def _log_report(self, report):
        entries = _load_log()
        entries.append(report)
        _save_log(entries)

    def get_recent_logs(self, count: int = 10) -> list:
        entries = _load_log()
        return entries[-count:]

    def get_dashboard(self) -> dict:
        logs = _load_log()
        latest = logs[-1] if logs else None
        return {
            "latest_check": latest,
            "total_checks": len(logs),
            "recent_actions": (
                latest.get("actions_taken", []) if latest else []
            ),
            "recent_alerts": (
                latest.get("alerts", []) if latest else []
            ),
            "overall_status": (
                latest.get("overall_status", "unknown") if latest else "unknown"
            ),
        }
