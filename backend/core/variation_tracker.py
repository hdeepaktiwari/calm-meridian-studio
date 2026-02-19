"""
Variation Tracker - Ensures visual variety across videos by tracking used dimensions
"""
import json
import random
from pathlib import Path
from datetime import datetime


class VariationTracker:
    """Tracks what dimensions were used in previous videos to ensure variety."""
    
    TRACKER_FILE = Path("variation_history.json")
    MAX_HISTORY = 10  # Check last N videos per domain
    
    def _load_history(self) -> dict:
        if self.TRACKER_FILE.exists():
            try:
                with open(self.TRACKER_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_history(self, history: dict):
        with open(self.TRACKER_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_fresh_identity(self, domain_name: str, domain=None) -> dict:
        """Returns a video identity that hasn't been used recently for this domain.
        
        If domain is provided, picks from domain's actual lists.
        Otherwise returns a structure with placeholder values.
        """
        history = self._load_history()
        domain_history = history.get(domain_name, [])[-self.MAX_HISTORY:]
        
        # Collect recently used values per dimension
        recent_values = {
            "time_period": set(),
            "season": set(),
            "weather_condition": set(),
            "narrative_theme": set(),
        }
        for entry in domain_history:
            for key in recent_values:
                val = entry.get(key)
                if val:
                    recent_values[key].add(val)
        
        recent_perspectives = set()
        for entry in domain_history:
            for p in entry.get("perspectives", []):
                recent_perspectives.add(p)
        
        def pick_fresh(options, recently_used):
            """Pick from options, preferring those not recently used."""
            fresh = [o for o in options if o not in recently_used]
            if fresh:
                return random.choice(fresh)
            return random.choice(options)
        
        if domain is None:
            # Return defaults for testing without a domain object
            return {
                "time_period": "golden hour",
                "season": "autumn peak",
                "weather_condition": "light fog",
                "perspectives": ["aerial drone", "ground level"],
                "narrative_theme": "solitude",
            }
        
        identity = {
            "time_period": pick_fresh(domain.time_periods, recent_values["time_period"]),
            "season": pick_fresh(domain.seasons, recent_values["season"]),
            "weather_condition": pick_fresh(domain.weather_conditions, recent_values["weather_condition"]),
            "narrative_theme": pick_fresh(domain.narrative_themes, recent_values["narrative_theme"]),
        }
        
        # Pick 2 perspectives, preferring fresh ones
        fresh_perspectives = [p for p in domain.perspectives if p not in recent_perspectives]
        if len(fresh_perspectives) >= 2:
            identity["perspectives"] = random.sample(fresh_perspectives, 2)
        elif len(fresh_perspectives) == 1:
            others = [p for p in domain.perspectives if p != fresh_perspectives[0]]
            identity["perspectives"] = fresh_perspectives + [random.choice(others)]
        else:
            identity["perspectives"] = random.sample(domain.perspectives, min(2, len(domain.perspectives)))
        
        return identity
    
    def record_identity(self, domain_name: str, identity: dict):
        """Record what identity was used for a video."""
        history = self._load_history()
        if domain_name not in history:
            history[domain_name] = []
        
        record = {**identity, "timestamp": datetime.now().isoformat()}
        history[domain_name].append(record)
        
        # Trim to last MAX_HISTORY * 2 entries
        if len(history[domain_name]) > self.MAX_HISTORY * 2:
            history[domain_name] = history[domain_name][-self.MAX_HISTORY:]
        
        self._save_history(history)
