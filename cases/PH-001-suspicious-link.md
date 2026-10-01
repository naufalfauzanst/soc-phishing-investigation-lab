# PH-001 — Suspicious Credential-Phishing Link

## Case Summary

| Field | Value |
|---|---|
| Case ID | PH-001 |
| Investigation date | 2026-10-01 |
| Analyst | Naufal |
| Severity | High |
| Verdict | True Positive — Authorized Phishing Simulation |
| Status | Closed |

## Executive Summary

A simulated email impersonated Microsoft Security and attempted to direct the recipient to an account-verification page. Analysis found a lookalike sender domain, mismatched email identities, failed SPF and DMARC checks, no DKIM signature, urgent social-engineering language, and a suspicious login URL.

The sample uses reserved domains and a documentation-only IP address. No live malicious infrastructure was accessed and no compromise occurred.

## Email Details

| Field | Value |
|---|---|
| From | `Microsoft Security <security-alert@micros0ft-support.example>` |
| Reply-To | `account-review@external-mail.example` |
| Return-Path | `bounce@external-mail.example` |
| Recipient | `employee@company.example` |
| Subject | `Urgent: Unusual sign-in detected` |
| Date | `2026-10-01 09:15:20 +0700` |
| Message-ID | `<ph001-20261001@external-mail.example>` |
| Source IP | `203.0.113.45` |

## Authentication Analysis

| Control | Result | Assessment |
|---|---|---|
| SPF | Fail | The sending infrastructure was not authorized for the envelope sender. |
| DKIM | None | The message did not contain a DKIM signature. |
| DMARC | Fail | The visible From domain did not pass authentication alignment. |

## Indicators

| Type | Indicator | Assessment |
|---|---|---|
| Domain | `micros0ft-support.example` | Lookalike sender domain using the number zero. |
| Domain | `external-mail.example` | Reply-To and Return-Path infrastructure. |
| IP address | `203.0.113.45` | Simulated source address from a documentation range. |
| URL | `hxxps://secure-account-review[.]example/login` | Simulated credential-phishing URL. |

## Analysis

### Sender impersonation

The display name claimed to be Microsoft Security, while the sender domain used `micros0ft` with the number zero. This lookalike naming pattern attempts to make the address appear legitimate during a quick review.

### Identity mismatch

The From, Reply-To, and Return-Path fields used different domains. A reply would be routed to infrastructure unrelated to the displayed sender identity.

### Authentication failure

SPF failed, DKIM was absent, and DMARC failed. The message therefore did not establish that the sender was authorized to represent the visible domain.

### Social engineering and link analysis

The subject and message threatened account suspension and demanded immediate action. The verification link did not point to an official Microsoft domain and was presented as an account login page. These characteristics are consistent with credential phishing.

Threat-intelligence reputation checks were not applicable because the indicators are reserved, non-operational values created for this simulation.

## Impact Assessment

The recipient did not click the simulated link or submit credentials. No endpoint or account compromise occurred. A successful real-world attempt could result in credential theft, session abuse, and unauthorized access to company resources.

## Verdict

**True Positive — Authorized Phishing Simulation**

The sender impersonation, identity mismatches, authentication failures, urgent language, and suspicious login URL collectively confirm a simulated credential-phishing attempt.

## Recommended Actions

- Quarantine the reported message.
- Search other mailboxes for the same sender, subject, URL, and Message-ID.
- Block confirmed malicious sender domains, URLs, and source infrastructure.
- Notify other recipients of matching messages.
- Reset credentials and revoke sessions if a recipient submitted credentials.
- Review authentication logs for suspicious sign-ins involving affected accounts.
- Preserve the original email and investigation evidence.

## MITRE ATT&CK Mapping

| Technique | ID |
|---|---|
| Phishing: Spearphishing Link | T1566.002 |

## Evidence

- [`PH-001-suspicious-email.txt`](../evidence/PH-001-suspicious-email.txt)
- [`01-ph001-suspicious-email.png`](../evidence/01-ph001-suspicious-email.png)
- [`02-ph001-header-analysis.png`](../evidence/02-ph001-header-analysis.png)
- [`03-ph001-ioc-table.png`](../evidence/03-ph001-ioc-table.png)
- [`indicators.csv`](../iocs/indicators.csv)
