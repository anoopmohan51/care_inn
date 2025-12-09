# filters/utils.py
from datetime import datetime
import pytz
from django.utils import timezone

class DataFormatter:
    @staticmethod
    def datetime(utc_time: datetime, date_type: str, _timezone: str):
        if not utc_time:
            return None
        try:
            local_tz = pytz.timezone(_timezone)
        except Exception:
            local_tz = timezone.get_current_timezone()

        if utc_time.tzinfo is None:
            # assume UTC if naive
            utc_time = utc_time.replace(tzinfo=pytz.utc)
        local_time = utc_time.astimezone(local_tz)

        if date_type == "date":
            return local_time.strftime("%m/%d/%Y")
        return local_time.strftime("%m/%d/%Y %I:%M %p")

def add_time_zone_for_date_between(condition: dict, tz_name: str):
    """
    Convert the 'value' for a date_between condition (expected as [start, end] or string)
    into timezone-aware datetimes in UTC to compare with DB fields (assuming DB stores UTC).
    Returns a mutated copy of condition (doesn't mutate original).
    """
    cond = condition.copy()
    try:
        value = cond.get("value")
        if not value:
            return cond

        # Expecting value as [start_str, end_str] or "start|end"
        if isinstance(value, str) and "|" in value:
            start_str, end_str = value.split("|", 1)
        elif isinstance(value, (list, tuple)) and len(value) == 2:
            start_str, end_str = value
        else:
            return cond

        tz = pytz.timezone(tz_name)
        # parse naive ISO-ish or common formats; be lenient
        def parse_dt(s):
            s = s.strip()
            dt = None
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    dt = datetime.strptime(s, fmt)
                    break
                except Exception:
                    continue
            if dt is None:
                # fallback — try Django/ISO parse via timezone
                try:
                    dt = datetime.fromisoformat(s)
                except Exception:
                    dt = None
            if dt is None:
                raise ValueError("unparsable date")
            # localize if naive, then convert to UTC
            if dt.tzinfo is None:
                dt = tz.localize(dt)
            return dt.astimezone(pytz.utc)

        start_utc = parse_dt(start_str)
        end_utc = parse_dt(end_str)
        cond["value"] = (start_utc, end_utc)
    except Exception:
        # if any parse error, keep original; caller should handle invalid filter values
        pass
    return cond
