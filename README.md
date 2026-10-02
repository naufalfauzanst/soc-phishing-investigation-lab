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
| [PH-002](cases/PH-002-spoofed-sender.md) | Spoofed finance sender | True Positive — Authorized Simulation | Complete |
| [PH-003](cases/PH-003-suspicious-attachment.md) | HTML invoice attachment | True Positive — Authorized Simulation | Complete |
| [PH-004](cases/PH-004-live-gmail-investigation.md) | Live Gmail delivery and header investigation | Benign — Authorized Training Email | Complete |

| [PH-005](cases/PH-005-live-gmail-attachment.md) | Live Gmail attachment detection in Splunk | True Positive — Authorized Simulation | Complete |

## PH-001 Key Findings

PH-001 covers a simulated email impersonating Microsoft Security. The investigation identified a lookalike sender domain, identity mismatches, failed SPF and DMARC checks, missing DKIM, urgent social-engineering language, and a suspicious login URL.

The sample uses reserved `.example` domains and the documentation IP range `203.0.113.0/24`. No live malicious infrastructure was accessed.

## PH-002 Key Findings

PH-002 covers a simulated finance-department impersonation requesting an urgent bank-account change. The investigation identified a spoofed internal From address, external Reply-To and Return-Path domains, an externally generated Message-ID, failed SPF and DMARC checks, missing DKIM, and payment-focused social engineering.

The sample uses reserved `.example` domains and the documentation IP range `198.51.100.0/24`. No real payment details or live infrastructure were used.

## PH-003 Key Findings

PH-003 analyzes a harmless HTML invoice attachment with a double extension, a work-account login request, and a defanged destination. File inspection and SHA-256 hashing identify the artifact. The synthetic headers record passing SPF, DKIM, and DMARC results, illustrating why content analysis remains necessary after authentication checks. No email delivery, credential collection, or compromise occurred.

## PH-004 Key Findings

PH-004 examines an email actually sent between two lab-owned Gmail accounts. Google reported SPF, DKIM, and DMARC as passing. The original EML was analyzed in the Windows VM and transferred to the host with a matching SHA-256. The case is classified as benign authorized training; no alert or compromise was demonstrated.

## PH-005 Key Findings

PH-005 links live Gmail delivery with the SOC homelab. Two harmless HTML invoice attachments were collected through Gmail API, indexed in Splunk through HTTPS HEC, and detected by DE-007. A scheduled digest alert triggered at 2026-10-02 14:47:01 with two results. Authentication passed for both messages; the detection matched the filename pattern rather than proving malware.

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
