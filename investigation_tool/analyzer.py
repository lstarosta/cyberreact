# analyzer.py
# Sends aggregated OSINT data to Claude for analysis.
# We're using the Claude API directly via requests — no SDK dependency.

import json
import requests
from investigation_tool.config import ANTHROPIC_API_KEY

ANALYSIS_PROMPT = """You are a cybersecurity analyst at a company that investigates online fraud and scam operations. You've just received raw OSINT data about a target domain from multiple sources.

Analyze the data below and produce a structured intelligence report. Be direct and specific — this report goes to both the cyber investigation team and the legal team.

Your report should include:

1. **SUMMARY** (2-3 sentences max — what is this domain, and should we be concerned?)

2. **RISK SCORE** (one of: Low / Medium / High / Critical — with a one-line justification)

3. **KEY FINDINGS** (bullet points — the most important things the investigator needs to know)

4. **CROSS-REFERENCES** (any connections you spotted across different data sources — e.g. same registrar patterns, suspicious timing, infrastructure overlap)

5. **RISK INDICATORS** (specific red flags, if any:
   - Domain age under 90 days
   - Privacy-shielded WHOIS
   - Hosting in high-risk jurisdictions
   - Free SSL on a site claiming to be a financial institution
   - Recently changed nameservers
   - Flagged by security vendors)

6. **RECOMMENDED NEXT STEPS** (2-4 concrete actions the team should take)

Here is the raw data:

{data}
"""


def analyze(domain, source_results):
    """Send aggregated OSINT data to Claude for analysis."""
    if not ANTHROPIC_API_KEY:
        return "ERROR: ANTHROPIC_API_KEY not set. Set it with: export ANTHROPIC_API_KEY=your_key"

    data_str = json.dumps(source_results, indent=2, default=str)
    prompt = ANALYSIS_PROMPT.format(data=data_str)

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )

        if resp.status_code != 200:
            error_data = resp.json().get("error", {}) if resp.text else {}
            msg = error_data.get("message", resp.text[:200])
            if "credit balance" in msg.lower():
                return "[AI analysis unavailable — API account needs credits. The raw findings above are complete.]"
            if resp.status_code == 401:
                return "[AI analysis unavailable — invalid API key. Set a valid key with: export ANTHROPIC_API_KEY=your_key]"
            return f"[AI analysis unavailable — API returned HTTP {resp.status_code}: {msg}]"

        content = resp.json().get("content", [])
        if content and content[0].get("type") == "text":
            return content[0]["text"]
        return "ERROR: Unexpected response format from Claude API"

    except requests.exceptions.Timeout:
        return "ERROR: Claude API request timed out after 30 seconds"
    except Exception as e:
        return f"ERROR: {str(e)}"
