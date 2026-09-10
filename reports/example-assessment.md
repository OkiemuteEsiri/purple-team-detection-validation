# Example Purple-Team Detection Validation Assessment

> Illustrative output based entirely on synthetic lab records.

## Executive summary

Four ATT&CK-aligned defensive exercises were reviewed. Two controls demonstrated complete expected telemetry and validated detection outcomes. One remote-access analytic was only partially observed because the expected logon-type field was absent. One endpoint-defense impairment scenario was missed and lacked sufficient supporting telemetry.

## Highest-priority gap

**PT-003 — T1562.001 Impair Defenses**

- Severity: Critical
- Outcome: Missed
- Expected telemetry: service change, endpoint control event, actor identity
- Observed telemetry: service change only
- Remediation owner: Detection Engineering
- Retest required: Yes

Recommended remediation is to validate collection of endpoint protection state-change events, preserve actor identity where available, review parser normalization, then re-run the authorized synthetic exercise and require analyst confirmation before closure.

## Secondary gap

**PT-002 — T1021.001 Remote Desktop Protocol**

The analytic produced a partial result because authentication, source-IP and destination-host context were present but logon-type telemetry was absent. The appropriate response is telemetry/parsing remediation rather than an unsupported claim that the control failed completely.

## Validated coverage

- PT-001 — T1059.001 PowerShell
- PT-004 — T1098 Account Manipulation

Both examples contain the complete expected telemetry set and analyst-confirmed detection outcomes.

## Closure criteria

A gap is closed only after the control change is implemented, the authorized exercise is repeated, required telemetry is observed, the analytic behaves as intended and an analyst validates the resulting evidence. A configuration change by itself is not treated as proof of risk reduction.
