# rdap.py
# RDAP lookup — the modern, structured alternative to WHOIS.
# No API key needed. Returns registration dates, registrar info, status codes.
# We're using ARIN's RDAP bootstrap which redirects to the right RDAP server for each TLD.

import requests


def lookup(domain):
    """Query RDAP for domain registration data."""
    try:
        resp = requests.get(
            f"https://rdap-bootstrap.arin.net/bootstrap/domain/{domain}",
            headers={"Accept": "application/rdap+json"},
            allow_redirects=True,
            timeout=10,
        )
        if resp.status_code != 200:
            return {"source": "RDAP", "error": f"HTTP {resp.status_code}", "domain": domain}

        data = resp.json()

        events = {e.get("eventAction"): e.get("eventDate") for e in data.get("events", [])}
        registrar = None
        for entity in data.get("entities", []):
            if "registrar" in entity.get("roles", []):
                vcard = entity.get("vcardArray", [None, []])[1]
                for field in vcard:
                    if field[0] == "fn":
                        registrar = field[3]
                        break

        return {
            "source": "RDAP",
            "domain": domain,
            "registrar": registrar,
            "registered": events.get("registration"),
            "last_updated": events.get("last changed"),
            "expires": events.get("expiration"),
            "status": data.get("status", []),
            "nameservers": [ns.get("ldhName") for ns in data.get("nameservers", [])],
        }

    except requests.exceptions.Timeout:
        return {"source": "RDAP", "error": "Request timed out", "domain": domain}
    except Exception as e:
        return {"source": "RDAP", "error": str(e), "domain": domain}
