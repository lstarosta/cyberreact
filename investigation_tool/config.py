# config.py
# API keys loaded from environment variables.
# We don't hardcode these — ever. Even for a demo.

import os

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", "")


def validate():
    """Check that required keys are set. Returns list of missing keys."""
    missing = []
    if not ANTHROPIC_API_KEY:
        missing.append("ANTHROPIC_API_KEY")
    # VirusTotal is optional — we skip it gracefully if the key isn't set
    return missing
