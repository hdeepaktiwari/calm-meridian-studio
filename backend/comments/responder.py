"""
Comment Responder — auto-replies to YouTube comments for Calm Meridian.
Brand voice: warm, peaceful, grateful. Like a calm friend.
"""
import json
import os
import re
import pickle
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from openai import OpenAI
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

IST = ZoneInfo("Asia/Kolkata")
STATE_FILE = Path("comment_responder_state.json")
MAX_REPLIED_IDS = 500
MAX_REPLIES_PER_CHECK = 20
MAX_REPLY_LENGTH = 200
CHANNEL_ID = "UCcE359PQPkiAjz6ht00d8Rg"

SYSTEM_PROMPT = """You run Calm Meridian, a chill ambient video channel on YouTube. You're a 25-year-old American creator who's genuinely passionate about calm, peaceful content. Reply to this viewer's comment like a real person — not a brand.

Rules:
- Keep it short: 1-3 sentences, UNDER 200 characters total
- Use casual American English — contractions, slang, natural speech
- First person "I" not "we" — you're one person, not a company
- Sound like a chill YouTuber who genuinely cares about their viewers
- NEVER sound corporate or formal. No "Thank you for your kind words" or "We appreciate your support"
- Casual punctuation is fine — "!!" and "..." and "haha" and "ngl"
- Emojis should feel natural, not decorative: 🌿 🌊 ✨ 🙏 💙
- If they mention a scene/moment, acknowledge it genuinely
- If they ask where something was filmed: the visuals are AI-generated but you try to capture the real feel
- Vary your responses — don't repeat the same vibe twice
- Use their name sometimes but not always
- If negative/spam, say SKIP

Good vibes: "honestly that means so much 💙 sleep well!" / "haha glad it hit different at night 🌊" / "yo welcome!! so happy you found us ✨"
Bad vibes (NEVER): "Thank you for your wonderful feedback!" / "We appreciate you taking the time..." / "Your support means the world to us"

Video: {video_title}
Category: {video_domain}
Commenter: {author_name}

Reply ONLY with the reply text (or SKIP). Nothing else."""


def _load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"enabled": True, "last_check": None, "replied_comment_ids": [], "total_replies": 0, "recent_replies": []}


def _save_state(state: dict):
    # Trim replied IDs
    if len(state.get("replied_comment_ids", [])) > MAX_REPLIED_IDS:
        state["replied_comment_ids"] = state["replied_comment_ids"][-MAX_REPLIED_IDS:]
    # Keep only last 50 recent replies
    if len(state.get("recent_replies", [])) > 50:
        state["recent_replies"] = state["recent_replies"][-50:]
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def _is_spam(text: str) -> bool:
    """Detect spam comments."""
    if not text:
        return True
    # Links
    if re.search(r'https?://|www\.', text, re.IGNORECASE):
        return True
    # ALL CAPS abuse (>80% caps and >20 chars)
    if len(text) > 20 and sum(1 for c in text if c.isupper()) / max(len(text.replace(" ", "")), 1) > 0.8:
        return True
    # Repetitive spam patterns
    spam_patterns = [r'check\s+my\s+channel', r'sub\s*4\s*sub', r'follow\s+me', r'visit\s+my']
    for p in spam_patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False


def _get_youtube():
    token_path = Path("youtube_token.pickle")
    if not token_path.exists():
        raise FileNotFoundError("youtube_token.pickle not found")
    with open(token_path, "rb") as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)
    return build("youtube", "v3", credentials=creds)


class CommentResponder:
    """Monitors YouTube comments and auto-replies with warm, on-brand responses."""

    def __init__(self):
        self._state = _load_state()

    def get_status(self) -> dict:
        s = _load_state()
        return {
            "enabled": s.get("enabled", True),
            "last_check": s.get("last_check"),
            "total_replies": s.get("total_replies", 0),
            "recent_replies_count": len(s.get("recent_replies", [])),
        }

    def toggle(self) -> bool:
        s = _load_state()
        s["enabled"] = not s.get("enabled", True)
        _save_state(s)
        return s["enabled"]

    def get_recent_replies(self, count: int = 20) -> list:
        s = _load_state()
        return list(reversed(s.get("recent_replies", [])))[:count]

    async def check_and_reply(self) -> dict:
        state = _load_state()
        result = {"checked": 0, "new_comments": 0, "replied": 0, "errors": 0}

        try:
            youtube = _get_youtube()
        except Exception as e:
            print(f"[COMMENTS] YouTube auth error: {e}")
            result["errors"] = 1
            return result

        replied_ids = set(state.get("replied_comment_ids", []))

        # Get own channel ID to skip own comments
        try:
            ch_resp = youtube.channels().list(mine=True, part="id").execute()
            own_channel_id = ch_resp["items"][0]["id"] if ch_resp.get("items") else CHANNEL_ID
        except Exception:
            own_channel_id = CHANNEL_ID

        # Fetch comment threads
        try:
            threads = []
            request = youtube.commentThreads().list(
                allThreadsRelatedToChannelId=CHANNEL_ID,
                part="snippet",
                maxResults=100,
                order="time",
            )
            response = request.execute()
            threads.extend(response.get("items", []))
            result["checked"] = len(threads)
        except Exception as e:
            print(f"[COMMENTS] Fetch error: {e}")
            result["errors"] += 1
            return result

        # Video title cache
        video_cache: dict = {}
        replies_this_run = 0

        for thread in threads:
            if replies_this_run >= MAX_REPLIES_PER_CHECK:
                break

            snippet = thread["snippet"]["topLevelComment"]["snippet"]
            comment_id = thread["snippet"]["topLevelComment"]["id"]
            author_name = snippet.get("authorDisplayName", "")
            author_channel = snippet.get("authorChannelId", {}).get("value", "")
            comment_text = snippet.get("textOriginal", "")
            video_id = snippet.get("videoId", "")

            # Skip already replied
            if comment_id in replied_ids:
                continue

            # Skip own comments
            if author_channel == own_channel_id:
                continue

            # Skip spam
            if _is_spam(comment_text):
                continue

            result["new_comments"] += 1

            # Get video info
            if video_id not in video_cache:
                try:
                    v_resp = youtube.videos().list(id=video_id, part="snippet").execute()
                    if v_resp.get("items"):
                        v_snip = v_resp["items"][0]["snippet"]
                        video_cache[video_id] = {
                            "title": v_snip.get("title", ""),
                            "domain": v_snip.get("categoryId", "Unknown"),
                        }
                    else:
                        video_cache[video_id] = {"title": "Unknown", "domain": "Ambient"}
                except Exception:
                    video_cache[video_id] = {"title": "Unknown", "domain": "Ambient"}

            v_info = video_cache[video_id]

            # Generate reply
            try:
                reply_text = await self.generate_reply(
                    comment_text, author_name, v_info["title"], v_info["domain"]
                )
            except Exception as e:
                print(f"[COMMENTS] Generate error: {e}")
                result["errors"] += 1
                continue

            if not reply_text or reply_text.strip().upper() == "SKIP":
                continue

            # Post reply
            try:
                self.post_reply(comment_id, reply_text)
                replies_this_run += 1
                result["replied"] += 1
                state["replied_comment_ids"].append(comment_id)
                state["total_replies"] = state.get("total_replies", 0) + 1
                state["recent_replies"].append({
                    "timestamp": datetime.now(IST).isoformat(),
                    "video_id": video_id,
                    "video_title": v_info["title"],
                    "comment_id": comment_id,
                    "author": author_name,
                    "comment_text": comment_text[:200],
                    "reply_text": reply_text,
                })
                print(f"[COMMENTS] Replied to {author_name}: {reply_text[:60]}...")
            except Exception as e:
                print(f"[COMMENTS] Post error: {e}")
                result["errors"] += 1

        state["last_check"] = datetime.now(IST).isoformat()
        _save_state(state)
        return result

    async def generate_reply(self, comment_text: str, author_name: str, video_title: str, video_domain: str) -> str:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(
                        video_title=video_title,
                        video_domain=video_domain,
                        author_name=author_name,
                    ),
                },
                {"role": "user", "content": comment_text},
            ],
            max_tokens=100,
            temperature=0.9,
        )
        reply = response.choices[0].message.content.strip()
        if reply.upper() == "SKIP":
            return "SKIP"
        # Enforce max length
        if len(reply) > MAX_REPLY_LENGTH:
            reply = reply[:MAX_REPLY_LENGTH].rsplit(" ", 1)[0]
        return reply

    def post_reply(self, parent_comment_id: str, reply_text: str) -> dict:
        youtube = _get_youtube()
        result = youtube.comments().insert(
            part="snippet",
            body={
                "snippet": {
                    "parentId": parent_comment_id,
                    "textOriginal": reply_text,
                }
            },
        ).execute()
        return result
