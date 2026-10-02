# PH-003 — Suspicious HTML Invoice Attachment

## Case Summary

| Field | Value |
|---|---|
| Case ID | PH-003 |
| Investigation date | 2026-10-02 |
| Analyst | Naufal |
| Scenario priority | High — simulated credential theft risk |
| Verdict | True Positive — Authorized Phishing Simulation |
| Status | Closed — static analysis complete |

## Executive Summary

A synthetic invoice email asked the recipient to open `Invoice-October.pdf.html` and sign in with a work account. Inspection confirmed that the attachment was an HTML document with a double extension. Its content displayed a login request and a defanged verification destination.

The supplied email text recorded SPF, DKIM, and DMARC as passing. These results were authored for the exercise; no receiving mail server or DNS checks independently verified them. The case demonstrates that sender-domain authentication does not establish whether message content is trustworthy.

## Scope and Limitations

This exercise analyzed locally created text and HTML files using PowerShell. No email was delivered. The attachment contains no scripts, forms, active links, downloads, or credential collection. No malware execution, user interaction, or compromise was observed. The verdict classifies the intended phishing scenario, not the harmless file as confirmed malware.

Public reputation checks were not performed because the domains and IP address are reserved training values.

## Email Details

| Field | Value |
|---|---|
| From | `Vendor Billing <invoices@vendor-billing.example>` |
| Reply-To | `help@vendor-billing.example` |
| Return-Path | `bounce@vendor-billing.example` |
| Recipient | `accounts-payable@company.example` |
| Subject | `October invoice - review attached document` |
| Date in sample | `2026-10-02 09:20:00 +0700` |
| Message-ID | `<ph003-20261002@vendor-billing.example>` |
| Source IP in sample | `192.0.2.88` |
| Attachment | `Invoice-October.pdf.html` |

## Authentication Review

| Control | Recorded result | Interpretation |
|---|---|---|
| SPF | Pass | The sample claims the envelope sender passed SPF. |
| DKIM | Pass | The sample claims a valid signature for `vendor-billing.example`. |
| DMARC | Pass | The sample claims authentication aligned with the visible From domain. |

The visible sender addresses use the same domain. A sender can authenticate a domain while distributing deceptive content. Passing authentication alone is insufficient to close a reported email as safe.

## Attachment Analysis

| Property | Observed value |
|---|---|
| Filename | `Invoice-October.pdf.html` |
| Actual extension | `.html` |
| File size | 484 bytes |
| Content | HTML document beginning with `<!DOCTYPE html>` |
| SHA-256 | `95F89ECBB7748673AB59615D08B940522C5C512E4D0B4867DE4F606579C970A7` |

The `.pdf` portion may suggest an invoice PDF, but the final extension and content identify HTML. The document asks for a work-account sign-in and displays `hxxps://invoice-access[.]example/login` as a claimed destination. This address appears only as defanged text.

The file was read as text rather than executed. Its hash identifies the exact training artifact and does not establish maliciousness or reputation.

## Extracted Indicators

| Type | Indicator | Assessment |
|---|---|---|
| Domain | `vendor-billing.example` | Simulated sender domain |
| Filename | `Invoice-October.pdf.html` | HTML attachment with double extension |
| IP | `192.0.2.88` | Simulated source IP |
| SHA-256 | `95F89ECBB7748673AB59615D08B940522C5C512E4D0B4867DE4F606579C970A7` | Hash of harmless training attachment |
| URL | `hxxps://invoice-access[.]example/login` | Simulated credential-phishing destination |

## Impact Assessment

No operational impact was demonstrated. In a real equivalent, a user following an invoice-themed login prompt could disclose work credentials. Mail, identity, proxy, and endpoint telemetry would be required to establish delivery, clicks, credential submission, or account misuse.

## Verdict

**True Positive — Authorized Phishing Simulation**

The double-extension invoice attachment and work-account login request support the intended credential-phishing scenario. The actual artifact is a harmless static training sample. Passing authentication results do not override the content findings.

## Recommended Response for a Real Incident

- Preserve the original email and attachment.
- Quarantine matching messages while confirming the invoice with the vendor through a known contact channel.
- Search mail logs for matching sender, Message-ID, subject, filename, and hash.
- Check browsing and identity logs for relevant activity.
- Block confirmed malicious destinations following validation.
- Reset exposed credentials and revoke sessions if credential submission is established.
- Record confirmed impact, actions taken, and remaining uncertainty.

These are recommendations; no live containment actions were performed in this exercise.

## Evidence

- [Email sample](../evidence/PH-003-suspicious-attachment-email.txt)
- [Static HTML attachment](../evidence/Invoice-October.pdf.html)
- [Email screenshot](../evidence/07-ph003-suspicious-email.png)
- [Attachment analysis](../evidence/08-ph003-attachment-analysis.png)
- [SHA-256 result](../evidence/09-ph003-file-hash.png)
- [Authentication results](../evidence/10-ph003-authentication-results.png)
- [Indicator list](../evidence/11-ph003-ioc-list.png)
- [IOC database](../iocs/indicators.csv)
