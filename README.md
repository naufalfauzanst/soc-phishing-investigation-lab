# SOC Phishing Investigation Lab

A hands-on SOC portfolio project focused on suspicious email analysis, indicator extraction, impact assessment, and response recommendations.

## Project Objectives

- Analyze email headers and authentication results.
- Identify suspicious sender infrastructure.
- Investigate URLs, domains, attachments, and file hashes.
- Record indicators of compromise (IOCs).
- Assign evidence-based verdicts and severity.
- Recommend containment and remediation actions.

## Investigation Cases

| Case | Scenario | Verdict | Status |
|---|---|---|---|
| [PH-001](cases/PH-001-suspicious-link.md) | Suspicious credential-phishing link | True Positive — Authorized Simulation | Complete |
| PH-002 | Spoofed sender | — | Planned |
| PH-003 | Suspicious attachment | — | Planned |

## PH-001 Key Findings

PH-001 covers a simulated email impersonating Microsoft Security. The investigation identified a lookalike sender domain, identity mismatches, failed SPF and DMARC checks, missing DKIM, urgent social-engineering language, and a suspicious login URL.

The sample uses reserved `.example` domains and the documentation IP range `203.0.113.0/24`. No live malicious infrastructure was accessed.

## Investigation Workflow

1. Preserve the original email evidence.
2. Review sender, Reply-To, and Return-Path identities.
3. Validate SPF, DKIM, and DMARC results.
4. Extract URLs, domains, IP addresses, and file hashes.
5. Enrich operational indicators with approved threat-intelligence sources.
6. Assess user interaction and possible impact.
7. Assign a verdict and document response actions.

## Repository Structure

- `cases/` — Completed investigation reports
- `evidence/` — Sanitized email samples and supporting evidence
- `iocs/` — Extracted indicators
- `playbooks/` — Phishing triage procedures
- `templates/` — Reusable investigation format

## Tools and Skills Demonstrated

- Email header analysis
- SPF, DKIM, and DMARC interpretation
- IOC extraction and documentation
- Phishing triage
- MITRE ATT&CK mapping
- Incident reporting
- PowerShell

## Safety

All cases use sanitized, simulated, or publicly available training data. Suspicious links and attachments are never opened directly on the host system.
