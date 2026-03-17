# dns_lookup.py
# Basic DNS resolution using Python's built-in socket library.
# No external API, no key, instant results.
# Gets us the IP address(es) the domain points to.

import socket


def lookup(domain):
    """Resolve domain to IP addresses."""
    try:
        results = socket.getaddrinfo(domain, None)
        ips = list(set(r[4][0] for r in results))

        return {
            "source": "DNS",
            "domain": domain,
            "ip_addresses": sorted(ips),
            "ip_count": len(ips),
        }

    except socket.gaierror as e:
        return {"source": "DNS", "error": f"DNS resolution failed: {e}", "domain": domain}
    except Exception as e:
        return {"source": "DNS", "error": str(e), "domain": domain}
