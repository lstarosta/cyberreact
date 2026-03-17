# virustotal.py
# VirusTotal domain lookup.
# Checks the domain against 70+ security vendors.
# Needs a free API key (sign up at virustotal.com, takes 30 seconds).
# If VIRUSTOTAL_API_KEY isn't set, we skip this source entirely.
# Free tier: 4 requests/minute — more than enough for a demo.

import requests
from investigation_tool.config import VIRUSTOTAL_API_KEY


def lookup(domain):
    """Query VirusTotal for domain reputation."""
    if not VIRUSTOTAL_API_KEY:
        return {"source": "VirusTotal", "skipped": True, "reason": "No API key set (VIRUSTOTAL_API_KEY)"}

    try:
        resp = requests.get(
            f"https://www.virustotal.com/api/v3/domains/{domain}",
            headers={"x-apikey": VIRUSTOTAL_API_KEY},
            timeout=10,
        )
        if resp.status_code == 401:
            return {"source": "VirusTotal", "error": "Invalid API key"}
        if resp.status_code != 200:
            return {"source": "VirusTotal", "error": f"HTTP {resp.status_code}", "domain": domain}

        data = resp.json().get("data", {}).get("attributes", {})
        stats = data.get("last_analysis_stats", {})

        return {
            "source": "VirusTotal",
            "domain": domain,
            "reputation_score": data.get("reputation", "N/A"),
            "malicious_detections": stats.get("malicious", 0),
            "suspicious_detections": stats.get("suspicious", 0),
            "harmless_detections": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
            "total_vendors": sum(stats.values()) if stats else 0,
            "categories": data.get("categories", {}),
        }

    except requests.exceptions.Timeout:
        return {"source": "VirusTotal", "error": "Request timed out", "domain": domain}
    except Exception as e:
        return {"source": "VirusTotal", "error": str(e), "domain": domain}
