# PH-002 — Spoofed Finance Sender

## Case Summary

| Field | Value |
|---|---|
| Case ID | PH-002 |
| Investigation date | 2026-10-01 |
| Analyst | Naufal |
| Severity | High |
| Verdict | True Positive — Authorized Sender Spoofing Simulation |
| Status | Closed |

## Executive Summary

A simulated email impersonated the internal Finance Department and instructed Accounts Payable to use new bank details for outstanding invoices. Header analysis showed that the visible internal sender identity did not match the external sending and reply infrastructure. SPF and DMARC failed, and the message had no DKIM signature.

The request used urgency, confidentiality, and instructions to avoid contacting the previous account manager. These findings are consistent with a business email compromise attempt designed to redirect payments.

All domains, IP addresses, and bank details in this case are reserved or simulated. No real payment or malicious infrastructure was involved.

## Email Details

| Field | Value |
|---|---|
| From | `Finance Department <finance@company.example>` |
| Reply-To | `payment-update@billing-secure.example` |
| Return-Path | `bounce@billing-secure.example` |
| Recipient | `accounts-payable@company.example` |
| Subject | `Urgent: Updated bank details for invoice settlement` |
| Date | `2026-10-01 11:42:08 +0700` |
| Message-ID | `<ph002-20261001@billing-secure.example>` |
| Source host | `outbound.billing-secure.example` |
| Source IP | `198.51.100.77` |

## Authentication Analysis

| Control | Result | Assessment |
|---|---|---|
| SPF | Fail | The external sending infrastructure was not authorized for the envelope sender. |
| DKIM | None | The message contained no verifiable DKIM signature. |
| DMARC | Fail | The visible `company.example` From domain did not pass authentication alignment. |

## Indicators

| Type | Indicator | Assessment |
|---|---|---|
| Email address | `payment-update@billing-secure.example` | External Reply-To address controlled by the simulated sender. |
| Domain | `billing-secure.example` | Reply, bounce, and Message-ID infrastructure. |
| Domain | `outbound.billing-secure.example` | Simulated sending host. |
| IP address | `198.51.100.77` | Simulated source address from a documentation range. |

## Analysis

### Spoofed internal identity

The visible From address claimed to be `finance@company.example`, presenting the message as an internal Finance Department request. However, the message was received from `outbound.billing-secure.example` at `198.51.100.77`.

### Reply-path mismatch

The Reply-To and Return-Path fields used `billing-secure.example`. A recipient pressing Reply would send the response to the external address rather than the displayed internal Finance address.

### Message origin mismatch

The Message-ID was generated under `billing-secure.example`, which further connected the message to the external infrastructure rather than the claimed internal domain.

### Authentication failure

SPF failed, DKIM was absent, and DMARC failed. The message did not prove that its sender was authorized to use the visible `company.example` identity.

### Social engineering

The message requested a change to payment instructions, demanded completion on the same day, described the request as confidential, and discouraged independent confirmation with the previous account manager. These tactics attempt to bypass normal payment-verification procedures.

Threat-intelligence reputation checks were not applicable because the indicators are reserved, non-operational values created for this simulation.

## Impact Assessment

No payment was initiated and no recipient replied to the simulated sender. No financial or account impact occurred. A successful real-world attempt could redirect invoice payments, expose financial information, and cause significant monetary loss.

## Verdict

**True Positive — Authorized Sender Spoofing Simulation**

The external sending infrastructure, mismatched reply path, failed email authentication, and payment-redirection request confirm a simulated sender-spoofing and business email compromise attempt.

## Recommended Actions

- Quarantine the message and search for matching sender, subject, Message-ID, and infrastructure indicators.
- Warn Accounts Payable and other recipients against processing the requested banking change.
- Verify financial requests through a trusted, previously established communication channel.
- Block confirmed malicious reply addresses, domains, and source infrastructure.
- Review mail logs for replies or similar messages sent to other recipients.
- Contact the finance team and affected vendors using known contact information.
- Preserve the original message and investigation evidence.
- Escalate immediately if any payment was attempted or completed.

## MITRE ATT&CK Mapping

| Technique | ID |
|---|---|
| Impersonation | T1656 |

## Evidence

- [`PH-002-spoofed-sender.txt`](../evidence/PH-002-spoofed-sender.txt)
- [`04-ph002-spoofed-email.png`](../evidence/04-ph002-spoofed-email.png)
- [`05-ph002-header-analysis.png`](../evidence/05-ph002-header-analysis.png)
- [`06-ph002-ioc-table.png`](../evidence/06-ph002-ioc-table.png)
- [`indicators.csv`](../iocs/indicators.csv)
