# report.py
# Formats and displays the final investigation report.
# Prints to terminal with some basic formatting, and saves a copy to a .txt file.

import json
from datetime import datetime


def print_report(domain, source_results, analysis):
    """Print the full investigation report to terminal."""
    separator = "=" * 70
    thin_sep = "-" * 70

    print(f"\n{separator}")
    print(f"  INVESTIGATION REPORT — {domain.upper()}")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{separator}\n")

    print(f"{'RAW FINDINGS':^70}")
    print(thin_sep)
    for result in source_results:
        source_name = result.get("source", "Unknown")
        if result.get("skipped"):
            print(f"\n[{source_name}] — Skipped: {result.get('reason', 'N/A')}")
        elif result.get("error"):
            print(f"\n[{source_name}] — Error: {result.get('error')}")
        else:
            print(f"\n[{source_name}]")
            for key, value in result.items():
                if key == "source":
                    continue
                if isinstance(value, list) and len(value) > 10:
                    print(f"  {key}: {value[:10]} ... (+{len(value)-10} more)")
                else:
                    print(f"  {key}: {value}")

    print(f"\n{separator}")
    print(f"{'AI ANALYSIS':^70}")
    print(f"{separator}\n")
    print(analysis)
    print(f"\n{separator}\n")


def save_report(domain, source_results, analysis, output_dir="."):
    """Save the report to a text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/report_{domain}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"INVESTIGATION REPORT — {domain.upper()}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("RAW FINDINGS\n")
        f.write("-" * 70 + "\n")
        f.write(json.dumps(source_results, indent=2, default=str))
        f.write("\n\n")

        f.write("AI ANALYSIS\n")
        f.write("=" * 70 + "\n")
        f.write(analysis)
        f.write("\n")

    return filename
