# wayback.py
# Wayback Machine availability API.
# Tells us when a site was first archived and when it was last seen.
# A scam site that appeared recently but already changed its content
# multiple times is a very different story from a 10-year-old business site.
# Free, no key needed.

import requests


def lookup(domain):
    """Check Wayback Machine for historical snapshots."""
    try:
        resp_first = requests.get(
            f"https://archive.org/wayback/available?url={domain}&timestamp=19700101",
            timeout=10,
        )
        resp_last = requests.get(
            f"https://archive.org/wayback/available?url={domain}&timestamp=20991231",
            timeout=10,
        )

        first_snapshot = None
        last_snapshot = None

        if resp_first.status_code == 200:
            snap = resp_first.json().get("archived_snapshots", {}).get("closest", {})
            if snap:
                first_snapshot = snap.get("timestamp", "")[:8]

        if resp_last.status_code == 200:
            snap = resp_last.json().get("archived_snapshots", {}).get("closest", {})
            if snap:
                last_snapshot = snap.get("timestamp", "")[:8]

        return {
            "source": "Wayback Machine",
            "domain": domain,
            "has_history": first_snapshot is not None,
            "earliest_snapshot": first_snapshot,
            "latest_snapshot": last_snapshot,
        }

    except requests.exceptions.Timeout:
        return {"source": "Wayback Machine", "error": "Request timed out", "domain": domain}
    except Exception as e:
        return {"source": "Wayback Machine", "error": str(e), "domain": domain}
