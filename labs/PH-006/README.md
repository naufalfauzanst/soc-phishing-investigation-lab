# PH-006 — Local HTML Form Submission Lab

This exercise demonstrates how an HTML attachment can instruct a browser to send form data to a separate server. The receiver represents the receiving side of a credential-phishing scenario. It runs only on `127.0.0.1`, with fixed fake values and no external destination or service branding.

## Run on the host

Open PowerShell in this folder:

```powershell
python .\receiver.py
```

Keep it open. Open `Invoice-Demo.pdf.html` in a browser on the same computer. Click **Kirim data latihan**. The fields are already filled with fake values. The server prints them in PowerShell and appends one event to `received-demo.jsonl`.

`localhost`/`127.0.0.1` refers to the computer running the browser. A browser in a VM cannot reach this host receiver using the same loopback address. Run both components on the host for this exercise.

Stop the receiver with Ctrl+C. Do not add real credentials. The receiver rejects values other than the exact built-in fake pair and does not record rejected values.

## Inspect evidence

```powershell
Get-Content .\received-demo.jsonl | ForEach-Object { $_ | ConvertFrom-Json } | Format-List
Get-FileHash .\Invoice-Demo.pdf.html -Algorithm SHA256
```

The recorded `password` is the public fake string `DEMO-NOT-A-REAL-PASSWORD`. It does not authenticate any account. The HTTP demonstration uses loopback; a real external HTTP submission would not protect transport contents.

## Validation already performed

`python .\receiver.py --self-test` sends a form-encoded POST with a Python HTTP client on a temporary loopback port, checks the evidence, then verifies unexpected values receive HTTP 400 without being recorded. The temporary server is stopped automatically.

See `validation.json` for checks and `received-demo.jsonl` for actual local receipt. The user separately followed the browser steps above. A second local receiver event at 2026-10-02T09:16:16.681785+00:00 confirms receipt of the same fake pair following that submission. The JSONL does not independently identify the browser. The user subsequently monitored this log in Splunk and validated a scheduled PH-006 alert at 16:30:01 UTC+07:00 with two results. Gmail delivery and account compromise were not established. See the case report for the separate Splunk validation.

## Splunk reproduction

Monitor this file with Splunk Web Files & Directories, sourcetype `_json`, index `email_security`, and constant host `ph006-local-lab`. Do not re-upload it on each submission. Use `alert.spl` without `spath`; `_json` already extracts the fields in the validated setup.

Save as a scheduled alert named `PH-006 Lab Form Submission Received`: cron `*/5 * * * *`, Last 10 minutes, Number of Results > 0, Once, Add to Triggered Alerts, Medium. Send another fake form submission while the receiver runs, then inspect Activity / Triggered Alerts after the next scheduled run.

`alert-results.csv` is a transcription of the user's scheduled View Results table, not a native export. `triggered-alert.png` is the supplied screenshot. Stop the local receiver after validation; disabling this lab alert later is optional and was not recorded as performed.
