# PH-006 — HTML Form Data Receipt Investigation

## Case Summary

| Field | Value |
|---|---|
| Analyst | Naufal |
| Scenario | Invoice-themed HTML attachment with a form submission destination |
| Verdict | Authorized local simulation; synthetic data receipt confirmed |
| Status | Closed — local receipt, file monitoring, and scheduled alert validated |
| Alert | PH-006 Lab Form Submission Received; Medium; 2026-10-02 16:30:01 UTC+07:00 |
| Scope | One host, loopback-only receiver, fixed fake data |

## Investigation Question

How can an HTML file send entered information to a receiver when HTML cannot directly write to a remote database?

The form defines a destination in `action` and a submission method in `method`. A browser reads those instructions and sends the fields in an HTTP request. A separate server receives the request and can store it. JavaScript is not required for this basic form submission.

## Artifacts and Static Findings

- Attachment: `Invoice-Demo.pdf.html`. The final extension is HTML, despite the preceding `.pdf`.
- Form destination: `http://127.0.0.1:9000/latihan`.
- Method: `POST`.
- Fields: `username` and `password`.
- Values: `user-lab` and `DEMO-NOT-A-REAL-PASSWORD`; both are fixed synthetic data.
- No JavaScript, external page assets, real login branding, or live attacker infrastructure.

The attachment uses a visible lab notice rather than impersonating a login page. A real adversary could place their server address in the form action. Here, the loopback receiver illustrates that receiving role on the same machine.

## Observed Evidence

The automated validation sent an actual URL-encoded HTTP POST using Python, equivalent to the form's field encoding. The receiver returned HTTP 200 and wrote one JSON record containing the fake username and password. A second request with different values returned HTTP 400 and created no additional record.

The validation server used a temporary loopback port; the browser exercise uses port 9000. Exact test timestamps and port are in `validation.json`. Server receipt time is in UTC and is not an email delivery or alert time.

After the user submitted the local HTML form in the browser, the receiver appended a second event at **2026-10-02T09:16:16.681785+00:00** (16:16:16 UTC+07:00). This event was confirmed in the local JSONL file and in the terminal output supplied by the user. The first event at 09:08:27 UTC belongs to the earlier automated test. The JSONL records server receipt, not a browser identity or packet capture; browser origin is supported by the user-reported reproduction steps.

The following pair was received by the simulated attacker-side component:

```text
username: user-lab
password: DEMO-NOT-A-REAL-PASSWORD
```

This is real local transport of invented data. It is not theft of real credentials. The program stores receipt in a JSONL file, not a database, demonstrating that a database is optional for receiving form data.

## Relationship to DE-007

The filename follows the `.pdf.html` pattern used in DE-007. PH-006 was not sent through Gmail or the Gmail collector. Its receiver log was monitored directly by Splunk on the host, separately from DE-007. PH-006 has its own scheduled alert evidence.

DE-007 flags attachment names. It does not establish form submission or credential disclosure. In a real investigation, correlate preserved attachment content with browser/network activity and recipient interaction.

## Splunk Monitoring and Scheduled Alert

The user configured Splunk Web Monitor / Files & Directories for `labs/PH-006/received-demo.jsonl`, with sourcetype `_json`, index `email_security`, and host `ph006-local-lab`. A search first showed the two existing records. After another browser submission, the user confirmed a third row; later scheduled results included the fourth record. This supports monitoring of appended log data.

With `_json`, field extraction already worked. Adding `spath` produced repeated field values; removing it restored one value per field in the validated table.

The [validated SPL](../labs/PH-006/alert.spl) matches lab host, case ID, POST method, and `/latihan` path. The alert runs on cron `*/5 * * * *`, with a 10-minute lookback, Number of Results > 0, Once/digest mode, and Add to Triggered Alerts at Medium severity. It does not display the password field.

| Time (UTC+07:00, 2026-10-02) | Evidence |
|---|---|
| 16:08:27.894 | Initial automated local HTTP test |
| 16:16:16.681 | User browser submission |
| 16:24:15.032 | Additional submission; included in scheduled result set |
| 16:27:34.133 | Alert-validation submission; included in scheduled result set |
| 16:30:01 | Scheduled Medium digest alert displayed in Triggered Alerts |

The user supplied the [Triggered Alerts screenshot](../labs/PH-006/triggered-alert.png) and pasted the scheduled View Results table. The [two-row transcription](../labs/PH-006/alert-results.csv) preserves the supplied results; it is not a native Splunk CSV export. Both event timestamps match records independently read from the local JSONL file. A separate filtered event-search screenshot shows the 16:27:34.133 record with host ph006-local-lab and sourcetype _json; it is supporting indexed-event evidence, not a screenshot of the two-row scheduled result table. The scheduled search covered 16:20:00 through 16:30:00.

This is a lab telemetry alert: it confirms that synthetic form submissions were recorded, indexed, and matched by the scheduled query. It is not a general phishing detector. Organizations usually cannot access a real attacker's receiving server logs; real-world detection would require available email, endpoint, proxy, or network telemetry. The overlapping lookback can repeat an alert for the same event on later runs; suppression was not validated.

## Impact and Verdict

The lab demonstrated receipt of the fixed synthetic values. No real username, password, Gmail account, remote attacker, or account compromise was involved. The lab-specific receipt alert matched the intended synthetic events. This validates the configured lab condition, not a verdict of malicious credential theft.

For a real external credential submission, assess exposed accounts, reset affected credentials, revoke relevant sessions, and review account access according to the organization's response process. These are recommendations; none were needed or performed for this local exercise.

## Reproduction and Cleanup

Follow the [local exercise instructions](../labs/PH-006/README.md). Run the receiver and browser on the same host. Stop the receiver with Ctrl+C after submission. The automated validation server stops itself. Preserve the fake-data JSONL as portfolio evidence; do not replace it with real credentials.

## Evidence

- [HTML attachment](../labs/PH-006/Invoice-Demo.pdf.html)
- [HTML training form screenshot](../labs/PH-006/html-training-form.png)
- [Local receiver](../labs/PH-006/receiver.py)
- [Recorded fake data](../labs/PH-006/received-demo.jsonl)
- [Receiver terminal screenshot](../labs/PH-006/receiver-terminal.png)
- [Validation checks](../labs/PH-006/validation.json)
- [Artifact hashes](../labs/PH-006/hashes.json)
- [Scheduled alert SPL](../labs/PH-006/alert.spl)
- [Triggered Alerts screenshot](../labs/PH-006/triggered-alert.png)
- [Indexed event search screenshot](../labs/PH-006/splunk-indexed-event.png)
- [Scheduled results transcription](../labs/PH-006/alert-results.csv)

## Limits

Email delivery, malicious execution, and account compromise were not established. Splunk receiver-log collection and a scheduled lab alert were validated. User browser submission was reproduced with a matching local receiver record; no browser network trace was captured. The filename is a triage signal, not a malware verdict. Do not treat `127.0.0.1` as an operational malicious indicator.
