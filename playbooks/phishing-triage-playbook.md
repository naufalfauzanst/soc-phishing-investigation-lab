# Phishing Email Triage Playbook

## Purpose

Provide a repeatable process for reviewing reported emails, determining risk, and recommending response actions.

## 1. Preserve Evidence

- Retain the original email in EML or MSG format when available.
- Record the reporting user, time received, subject, sender, and Message-ID.
- Store sanitized screenshots and extracted indicators in the case folder.
- Do not open suspicious links or attachments on the analyst workstation.

## 2. Review Sender Identity

- Compare the display name with the actual From address.
- Inspect Reply-To and Return-Path for mismatches.
- Look for misspellings, lookalike domains, and unusual top-level domains.
- Determine whether the sender is expected to contact the recipient.

## 3. Review Email Authentication

- Check SPF, DKIM, and DMARC results.
- Review alignment between the visible From domain and authenticated domains.
- Treat authentication results as supporting evidence rather than a verdict by themselves.

## 4. Analyze Content

- Identify urgency, threats, payment requests, credential requests, or unusual instructions.
- Compare the claimed organization with the linked domains.
- Note unexpected attachments, password-protected archives, macros, and executable content.

## 5. Extract and Enrich Indicators

- Extract sender addresses, domains, URLs, IP addresses, attachment names, and hashes.
- Defang URLs before documenting them.
- Use approved reputation and sandbox services only when policy permits.
- Do not submit confidential email content or internal documents to public services.

## 6. Assess User and Environment Impact

- Determine whether the recipient clicked a link, opened an attachment, entered credentials, or executed a file.
- Search mailboxes, proxy logs, DNS logs, endpoint telemetry, and identity logs for matching activity.
- Identify all affected users and systems.

## 7. Assign a Verdict

- **True Positive:** The email demonstrates malicious or simulated malicious behavior.
- **False Positive:** The alert or report was incorrect and the email is legitimate.
- **Benign Positive:** The detection correctly matched behavior that was authorized or expected.

## 8. Respond

- Quarantine or remove matching messages.
- Block confirmed malicious indicators.
- Reset credentials and revoke sessions after suspected credential exposure.
- Isolate endpoints after suspected malware execution.
- Notify affected users and preserve evidence.
- Escalate according to severity and organizational policy.

## 9. Close the Case

- Record the final verdict and evidence.
- Document actions taken and any remaining risk.
- Update detection logic or user-awareness guidance when useful.
- Confirm that investigation artifacts contain no secrets or sensitive personal data before publishing.
