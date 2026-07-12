import json
import os
import sys
from collections import defaultdict
import markdown

# --- 1. CONFIGURATION & MAPPING ---
INPUT_FILE = "final_merged_scan.report.jsonl"
OUTPUT_HTML = "security_posture_report.html"

DOMAIN_MAPPING = {
    "dan": "Prompt Injection & Jailbreaks",
    "promptinject": "Prompt Injection & Jailbreaks",
    "tap": "Prompt Injection & Jailbreaks",
    "suffix": "Prompt Injection & Jailbreaks",
    "visual_jailbreak": "Prompt Injection & Jailbreaks",
    "encoding": "Prompt Injection & Jailbreaks",
    "ansiescape": "Prompt Injection & Jailbreaks",
    "badchars": "Prompt Injection & Jailbreaks",
    "divergence": "Prompt Injection & Jailbreaks",
    "doctor": "Prompt Injection & Jailbreaks",
    "dra": "Prompt Injection & Jailbreaks",
    "glitch": "Prompt Injection & Jailbreaks",
    "smuggling": "Prompt Injection & Jailbreaks",
    "agent_breaker": "Prompt Injection & Jailbreaks",
    "goodside": "Prompt Injection & Jailbreaks",
    "leakreplay": "Data Privacy & Exfiltration",
    "propile": "Data Privacy & Exfiltration",
    "web_injection": "Data Privacy & Exfiltration",
    "sysprompt_extraction": "Data Privacy & Exfiltration",
    "apikey": "Data Privacy & Exfiltration",
    "realtoxicityprompts": "Toxicity & Harmful Content",
    "lmrc": "Toxicity & Harmful Content",
    "donotanswer": "Toxicity & Harmful Content",
    "atkgen": "Toxicity & Harmful Content",
    "grandma": "Toxicity & Harmful Content",
    "continuation": "Toxicity & Harmful Content",
    "topic": "Toxicity & Harmful Content",
    "malwaregen": "Cyber Exploitation & Malware",
    "exploitation": "Cyber Exploitation & Malware",
    "av_spam_scanning": "Cyber Exploitation & Malware",
    "misleading": "Hallucination & Misinformation",
    "packagehallucination": "Hallucination & Misinformation",
    "snowball": "Hallucination & Misinformation",
    "latentinjection": "Hallucination & Misinformation",
    "fitd": "Hallucination & Misinformation",
    "goat": "Hallucination & Misinformation",
    "phrasing": "Hallucination & Misinformation",
    "phraising": "Hallucination & Misinformation"
}

# --- 2. DATA PROCESSING ---
def process_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: Could not find {file_path}")
        sys.exit(1)

    metadata = {"model": "Merged Multi-Scan", "time": "Multiple"}
    domain_totals = defaultdict(lambda: {"passed": 0, "total": 0})
    domain_stats = defaultdict(list)
    global_passed, global_total = 0, 0
    lines_processed = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            lines_processed += 1
            try:
                data = json.loads(line)
                etype = data.get("entry_type")

                # Grab the first model name we see
                if etype == "start_run setup" and metadata["model"] == "Merged Multi-Scan":
                    metadata['model'] = data.get("plugins.target_name", "Unknown Model")

                elif etype == "eval":
                    probe_name = data.get('probe', 'Unknown')
                    category = probe_name.split('.')[0] if '.' in probe_name else 'uncategorized'
                    domain = DOMAIN_MAPPING.get(category, "Other Anomalies")
                    
                    passed, total, fails = data.get('passed', 0), data.get('total_evaluated', 0), data.get('fails', 0)
                    score = (passed / total) * 100 if total > 0 else 0
                    
                    domain_totals[domain]["passed"] += passed
                    domain_totals[domain]["total"] += total
                    global_passed += passed
                    global_total += total
                    
                    domain_stats[domain].append({"probe": probe_name, "passed": passed, "fails": fails, "total": total, "score": score})

            except (json.JSONDecodeError, KeyError):
                continue
                
    return metadata, domain_totals, domain_stats, global_passed, global_total, lines_processed

# --- 3. GENERATE HTML ---
def build_html():
    print("Processing merged JSONL file...")
    meta, totals, stats, g_pass, g_tot, line_count = process_data(INPUT_FILE)
    print(f"Processed {line_count} lines. Found {g_tot} evaluations.")
    
    if g_tot == 0:
        print("Error: No 'eval' records found. The merged file might be incomplete.")
        sys.exit(1)

    g_score = (g_pass / g_tot) * 100

    # Build Markdown String
    md = []
    md.append(f"# LLM Security Posture Report")
    md.append(f"**Target Model:** `{meta['model']}` | **Scanned Iterations:** Multiple\n---")
    
    md.append(f"## Executive Summary")
    md.append(f"> **Overall Guardrail Efficacy:** **{g_score:.1f}%**\n")
    
    md.append(f"## Security Posture by Domain")
    md.append("| Security Domain | Vulnerable / Tested | Pass Rate |")
    md.append("| :--- | :---: | :---: |")
    for d, t in sorted(totals.items()):
        d_score = (t["passed"] / t["total"]) * 100 if t["total"] > 0 else 0
        md.append(f"| **{d}** | {t['total'] - t['passed']} / {t['total']} | {d_score:.1f}% |")
    
    md.append(f"\n## Vulnerability Detail by Probe")
    for d, s_list in sorted(stats.items()):
        # Output Domain Heading
        md.append(f"### {d}")
        
        # Output one table per Domain containing all its probes
        md.append("| Probe Name | Tested | Blocked | Bypassed | Pass Rate |")
        md.append("| :--- | :---: | :---: | :---: | :---: |")
        
        # Sort probes within the domain by score (lowest/riskiest first)
        for s in sorted(s_list, key=lambda x: x['score']):
            md.append(f"| `{s['probe']}` | {s['total']} | {s['passed']} | {s['fails']} | **{s['score']:.1f}%** |")
        
        md.append("\n") # Add spacing after the table

    md_text = "\n".join(md)
    html_body = markdown.markdown(md_text, extensions=['tables'])
    
    # CSS Styling
    styled_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Security Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; line-height: 1.6; margin: 40px auto; max-width: 1000px; color: #333; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 30px; border-bottom: 1px solid #eee; }}
        h3 {{ color: #2c3e50; margin-top: 35px; background: #f4f8fa; padding: 10px; border-left: 5px solid #3498db; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0 35px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        /* Align the first column (Probe Name/Domain) to the left */
        td:first-child, th:first-child {{ text-align: left; }}
        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; color: #e74c3c; }}
    </style></head><body>{html_body}</body></html>"""
    
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(styled_html)
    print(f"Success! HTML report successfully generated: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_html()