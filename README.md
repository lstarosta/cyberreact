# Investigation Intelligence Tool

OSINT aggregation tool for cybersecurity investigations. Takes a domain as input, queries multiple data sources in parallel, and uses AI to cross-reference findings and produce a structured intelligence report.

## How it works

1. Analyst enters a target domain
2. Tool queries 5 OSINT sources in parallel (RDAP, crt.sh, Wayback Machine, DNS, VirusTotal)
3. Results are sent to Claude for cross-referencing, risk scoring, and analysis
4. Structured report is printed to terminal and saved to file

## Setup

```bash
pip install -r investigation_tool/requirements.txt

# Required
export ANTHROPIC_API_KEY=your_key_here

# Optional (VirusTotal lookup will be skipped if not set)
export VIRUSTOTAL_API_KEY=your_key_here
```

## Usage

```bash
python3 -m investigation_tool.investigate example.com
```

## Data Sources

- **RDAP** — domain registration data (registrar, dates, nameservers). No API key needed.
- **crt.sh** — SSL certificate transparency logs. Reveals subdomains and connected domains. No API key needed.
- **Wayback Machine** — historical site snapshots. No API key needed.
- **DNS** — IP resolution via Python stdlib. No API key needed.
- **VirusTotal** — threat intelligence from 70+ security vendors. Free API key from virustotal.com.

## Architecture

Each data source is a separate module in `sources/` that returns a dict. If a source fails, it returns an error dict instead of crashing — the report still generates with the remaining sources.

The AI analysis layer (Claude API) cross-references findings across sources, flags risk indicators, assigns a risk score, and suggests next steps.
