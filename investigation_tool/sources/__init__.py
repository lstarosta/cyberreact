from .rdap import lookup as rdap_lookup
from .crtsh import lookup as crtsh_lookup
from .wayback import lookup as wayback_lookup
from .dns_lookup import lookup as dns_lookup
from .virustotal import lookup as virustotal_lookup

# All source functions in one list — the main script iterates over these.
# Each returns a dict. If a source fails, it returns a dict with an "error" key.
# This means the report always generates, even if some sources are down.
ALL_SOURCES = [
    ("RDAP (WHOIS)", rdap_lookup),
    ("crt.sh (SSL Certs)", crtsh_lookup),
    ("Wayback Machine", wayback_lookup),
    ("DNS Resolution", dns_lookup),
    ("VirusTotal", virustotal_lookup),
]
