#!/usr/bin/env python3
# investigate.py
# Main entry point for the investigation tool.
#
# Usage:
#   python3 -m investigation_tool.investigate example.com
#
# Required:
#   export ANTHROPIC_API_KEY=your_key
#
# Optional:
#   export VIRUSTOTAL_API_KEY=your_key  (for VirusTotal lookups)

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from investigation_tool.sources import ALL_SOURCES
from investigation_tool.analyzer import analyze
from investigation_tool.report import print_report, save_report
from investigation_tool import config


def run_sources(domain):
    """Run all OSINT sources in parallel and collect results."""
    results = []

    print(f"\nQuerying {len(ALL_SOURCES)} sources for: {domain}")
    print("-" * 40)

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_name = {
            executor.submit(fn, domain): name
            for name, fn in ALL_SOURCES
        }

        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                result = future.result()
                if result.get("error"):
                    status = "ERROR"
                elif result.get("skipped"):
                    status = "SKIPPED"
                else:
                    status = "DONE"
                print(f"  [{status:>7}] {name}")
                results.append(result)
            except Exception as e:
                print(f"  [  ERROR] {name}: {e}")
                results.append({"source": name, "error": str(e)})

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m investigation_tool.investigate <domain>")
        print("Example: python3 -m investigation_tool.investigate example.com")
        sys.exit(1)

    domain = sys.argv[1].strip().lower()

    # Strip protocol if someone pastes a full URL
    if domain.startswith("http://"):
        domain = domain[7:]
    if domain.startswith("https://"):
        domain = domain[8:]
    domain = domain.rstrip("/")

    # Check required keys
    missing = config.validate()
    if missing:
        print(f"Missing required environment variable(s): {', '.join(missing)}")
        print("Set them with:")
        for key in missing:
            print(f"  export {key}=your_key_here")
        sys.exit(1)

    # Step 1: Gather data from all sources
    source_results = run_sources(domain)

    # Step 2: Send to Claude for analysis
    print(f"\nSending {len(source_results)} source results to Claude for analysis...")
    analysis = analyze(domain, source_results)

    # Step 3: Display and save
    print_report(domain, source_results, analysis)

    filepath = save_report(domain, source_results, analysis,
                           output_dir="/Users/lstarosta/cyberreact/investigation_tool")
    print(f"Report saved to: {filepath}")


if __name__ == "__main__":
    main()
