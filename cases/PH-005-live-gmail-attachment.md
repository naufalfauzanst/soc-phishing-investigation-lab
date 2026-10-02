# PH-005 — Live Gmail Attachment Detection with Splunk

## Case Summary

| Field | Value |
|---|---|
| Investigation date | 2026-10-02 |
| Analyst | Naufal |
| Severity | Medium |
| Verdict | True Positive — Authorized Attack Simulation |
| Status | Closed — delivery, ingestion, and scheduled detection validated |
| Related detection | DE-007 Suspicious Email Attachment Double Extension |
| Alert time | 2026-10-02 14:47:01 SE Asia Standard Time |

## Summary

Two live emails were sent between lab-owned Gmail accounts with the harmless `Invoice-October.pdf.html` training attachment. A read-only Gmail API collector running on the host extracted selected message metadata and sent it through HTTPS HEC into Splunk's `email_security` index. A scheduled DE-007 search produced a digest alert with two results.

The analyst reviewed Gmail in the Windows VM. Collector ingestion runs on the host and does not depend on the Gmail browser staying open. This case connects the phishing-investigation and SOC detection repositories.

## Account Privacy

The sender and analyst addresses are represented as `user.sender@gmail.com` and `user.analyst@gmail.com`. These are placeholders. Full addresses, OAuth secrets, HEC tokens, raw email identifiers, and private TLS keys are excluded from the public evidence.

## Timeline

| Time shown by Splunk | Evidence |
|---|---|
| 2026-10-02 13:34:04 | Earlier baseline email: no attachment, double-extension flag false |
| 2026-10-02 14:41:35 | PH-005 invoice email with HTML attachment |
| 2026-10-02 14:46:04 | New PH-005 alert-validation email with the same filename pattern |
| 2026-10-02 14:47:01 | Scheduled digest alert displayed in Triggered Alerts |
| 2026-10-02 14:47:01.496 | Scheduler reported success and two results |

Collection and scheduling times are distinct from email timestamps. Precise end-to-end latency was not measured. Inbox-versus-spam placement was not separately recorded.

## Email and Authentication Findings

| Property | Invoice email | Validation email |
|---|---|---|
| Subject | [SOC LAB] PH-005 Invoice overdue — action required today | [SOC LAB] PH-005 Alert validation |
| Sender domain | gmail.com | gmail.com |
| Attachment | Invoice-October.pdf.html | Invoice-October.pdf.html |
| SPF / DKIM / DMARC | Pass / Pass / Pass | Pass / Pass / Pass |
| Double-extension detection | true | true |

The invoice-themed subject and `.pdf.html` filename provided the suspicious pattern. Passing authentication shows why authentication alone cannot decide whether an attachment warrants investigation.

## Attachment Context

PH-003 previously established that the local source attachment is a 484-byte static HTML file containing a simulated work-account login prompt and a defanged destination. The file has no scripts, forms, active links, or credential collection.

Source-file SHA-256:

`95F89ECBB7748673AB59615D08B940522C5C512E4D0B4867DE4F606579C970A7`

The collector analyzes MIME attachment names, not attachment bytes. The recipient-side attachment was not downloaded and rehashed during PH-005; the source hash is contextual evidence rather than proof of recipient-copy integrity.

## Splunk Validation

The Gmail API collector returned successful HEC acceptance for each new email. Indexed searches confirmed the baseline and PH-005 metadata. A JSON field-extraction duplication issue was corrected in the SPL using `mvdedup`; unique messages are identified with hashed Gmail IDs.

Validated message hashes:

- Invoice email: `40437ba0a51273530f226eb20e08427e0c133337083c876a0e5ff3de01f99912`
- Validation email: `1088c51b167df53596111e44cf0c80a8a48810bb04bdaffea1a218e44d1fa026`

DE-007 ran on cron `2-59/5 * * * *` with a 15-minute lookback, a result-count threshold greater than zero, and Add to Triggered Alerts enabled at Medium severity. The screenshot confirms two rows in the scheduled result set.

## Verdict and Impact

**True Positive — Authorized Attack Simulation**, because the alert correctly matched the intended suspicious filename pattern. No malicious attachment execution, credential disclosure, or account compromise was established. The actual file remains a harmless training artifact.

No automated blocking, deletion, or credential reset was performed. For a real incident, preserve the original message, verify the invoice through a known contact, inspect the attachment in isolation, and review recipient activity before determining impact.

## Evidence

- [Baseline Gmail-to-Splunk ingestion](../evidence/15-gmail-splunk-ingestion.png)
- [DE-007 Triggered Alerts](../evidence/16-de007-triggered-alert.png)
- [Scheduled alert results](../evidence/17-de007-alert-results.png)
- [PH-003 static attachment analysis](PH-003-suspicious-attachment.md)
- [PH-004 baseline Gmail investigation](PH-004-live-gmail-investigation.md)
- [DE-007 detection query and limitations](https://github.com/naufalfauzanst/soc-splunk-detection-lab/blob/main/detections/DE-007-email-attachment-double-extension.md)
- [IR-007 SOC investigation](https://github.com/naufalfauzanst/soc-splunk-detection-lab/blob/main/investigations/IR-007-email-attachment-double-extension.md)
- [Collector implementation](https://github.com/naufalfauzanst/soc-splunk-detection-lab/tree/main/integrations/gmail)

## Lessons Learned

- Real Gmail messages can be collected independently of the recipient's browser through read-only OAuth.
- HEC acceptance must be followed by an indexed search and scheduler evidence.
- Email authentication does not establish attachment safety.
- Filename-based alerts require content review and context to determine maliciousness.
- A manually run collector provides ingestion only when executed; continuous operation remains unvalidated.
