# PH-004 — Live Gmail Email Investigation

## Case Summary

| Field | Value |
|---|---|
| Case ID | PH-004 |
| Investigation date | 2026-10-02 |
| Analyst | Naufal |
| Classification | Benign — authorized training email |
| Severity | Informational |
| Status | Closed — email and header analysis complete |

## Executive Summary

An authorized training message was sent between two analyst-owned Gmail accounts and examined in the Windows SOC VM. The original EML was downloaded, its headers inspected with PowerShell, and its SHA-256 calculated. Google reported passing SPF, DKIM, and DMARC results.

The message contains an invoice-themed prompt and a defanged documentation URL. It explicitly states that it is a training message and requests no credentials or payment. No attachment or active credential-collection page was included.

This case demonstrates real email delivery, preservation, authentication review, and evidence integrity. It does not demonstrate sender spoofing, malware execution, or detection by a SOC alert.

## Environment and Workflow

- Sender: Gmail account opened on the host computer.
- Recipient: Gmail account opened in the Windows SOC VM.
- Evidence: original email downloaded using Gmail's Show original page.
- Analysis: PowerShell header extraction and SHA-256 calculation in the VM.
- Preservation: EML transferred to the host repository and rehashed.

Inbox-versus-spam placement was not recorded. Sysmon and Splunk telemetry were not collected for this case.

## Email Details

| Field | Observed value |
|---|---|
| From | `Lab Sender <user.sender@gmail.com>` |
| To | `user.analyst@gmail.com` |
| Return-Path | `<user.sender@gmail.com>` |
| Subject, decoded | `[SOC LAB] Invoice review — email investigation test` |
| Date header | `Fri, 2 Oct 2026 13:34:04 +0700` |
| Message-ID | `<REDACTED@mail.gmail.com>` |
| Content-Type | `multipart/alternative` |
| Authentication service | `mx.google.com` |
| Sending server IP in SPF result | `209.85.220.41` |

The Date header is recorded exactly as found. Gmail's screenshot shows a different display time; timezone and display configuration were not independently reconciled. The sending server IP is an email transport indicator, not evidence of the user's workstation IP.

## Authentication Findings

| Control | Result | Supporting fields |
|---|---|---|
| SPF | Pass | `smtp.mailfrom=user.sender@gmail.com`; permitted sending IP `209.85.220.41` |
| DKIM | Pass | `header.i=@gmail.com`; selector `20251104` |
| DMARC | Pass | `header.from=gmail.com` |

The From and Return-Path addresses match. Google recorded successful sender-domain authentication. Authentication supports domain legitimacy; message content still requires review.

The EML also contains ARC authentication results, which accounts for repeated authentication lines in the extraction output. The receiver's `Authentication-Results: mx.google.com` provides the results used in this report.

## Content Review

The plain-text and HTML alternatives contain the same invoice-themed training message. The URL `hxxps://invoice-review[.]example/login` is defanged and uses a reserved domain. The body explicitly identifies the message as an authorized SOC exercise.

No file attachment is present in the examined MIME structure. No real login destination or credential-submission mechanism was established.

## Evidence Integrity

| Property | Value |
|---|---|
| Original filename | `PH-004-live-gmail.eml` |
| Algorithm | SHA-256 |
| Hash recorded in VM | `8C515C6C57598B0A850A2B7BFA2D0AF979ED437E1C05CB797E23848F72576FCD` |
| Hash calculated on host | `8C515C6C57598B0A850A2B7BFA2D0AF979ED437E1C05CB797E23848F72576FCD` |
| Transfer verification | Match |

The matching hashes verify that the transferred EML is byte-for-byte identical to the file hashed in the VM. Hash equality does not independently prove authenticity or maliciousness.

## Verdict and Limitations

**Benign — authorized training email.**

The email was deliberately sent between lab-owned accounts, passed receiver authentication, and explicitly disclosed its training purpose. No compromise was established. No alert was evaluated, so true-positive or false-positive detection labels are not assigned.

No reputation lookup, sandbox detonation, phishing-page hosting, credential capture, or endpoint incident response was performed. No ATT&CK execution is claimed.

## Evidence

- [Sanitized header and message excerpt](../evidence/PH-004-sanitized-email.txt)

Public evidence uses `user.sender@gmail.com` and `user.analyst@gmail.com` as placeholders. These are not the actual lab account addresses. The original Message-ID is redacted. Original EML and screenshots are preserved locally and excluded from Git.

The original EML hash above applies to the private original only. The public text excerpt is a transformed artifact and cannot be used to independently verify the original DKIM signature.

## Lessons Learned

- A real EML preserves transport headers and MIME content for repeatable analysis.
- Passing SPF, DKIM, and DMARC results do not replace content review.
- A file hash validates transfer integrity when compared against the preserved source hash.
- An authorized training email should not be described as a confirmed phishing incident or detector true positive without corresponding evidence.
