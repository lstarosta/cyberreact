# crtsh.py
# Certificate transparency lookup via crt.sh.
# Free, no key needed. Returns all SSL certs issued for a domain,
# which reveals subdomains and sometimes connected domains.
# If a scam site has certs for other domains too, you've just found
# the rest of the operation.

import requests


def lookup(domain):
    """Query crt.sh for certificate transparency data."""
    try:
        resp = requests.get(
            f"https://crt.sh/?q={domain}&output=json",
            timeout=20,
        )
        if resp.status_code != 200:
            return {"source": "crt.sh", "error": f"HTTP {resp.status_code}", "domain": domain}

        certs = resp.json()

        # Deduplicate — we care about unique domains, not every cert renewal
        unique_names = set()
        for cert in certs:
            name = cert.get("common_name", "")
            if name:
                unique_names.add(name.lower())
            for nv in cert.get("name_value", "").split("\n"):
                if nv.strip():
                    unique_names.add(nv.strip().lower())

        sorted_names = sorted(unique_names)[:50]

        return {
            "source": "crt.sh",
            "domain": domain,
            "total_certs_found": len(certs),
            "unique_domains_and_subdomains": sorted_names,
            "sample_count": len(sorted_names),
        }

    except requests.exceptions.Timeout:
        return {"source": "crt.sh", "error": "Request timed out (crt.sh can be slow)", "domain": domain}
    except Exception as e:
        return {"source": "crt.sh", "error": str(e), "domain": domain}
