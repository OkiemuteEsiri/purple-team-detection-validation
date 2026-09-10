# Architecture and Validation Methodology

## Purpose

This project models a controlled purple-team detection-validation workflow. It does not execute attacks. Instead, it evaluates synthetic, authorized exercise records against expected telemetry, analytic outcomes, analyst validation and retest requirements.

## Architecture

1. `data/synthetic_exercises.json` contains exercise definitions and synthetic observations.
2. `src/models.py` provides immutable validated domain models.
3. `src/engine.py` calculates telemetry coverage, deterministic finding IDs, bounded contextual risk and portfolio metrics.
4. `src/reporting.py` renders an analyst- and recruiter-readable Markdown assessment.
5. `tests/test_engine.py` validates model constraints, scoring, duplicate handling, reporting and deterministic behavior.
6. GitHub Actions performs compile and unit-test checks with read-only repository permissions.

## Validation workflow

### 1. Plan
Define an authorized exercise, ATT&CK technique, control objective, expected telemetry and success criteria before execution in an isolated lab.

### 2. Observe
Record only the synthetic/authorized telemetry expected from the exercise. This repository stores representative observations rather than offensive payloads.

### 3. Evaluate
Classify the detection outcome as `detected`, `partial`, `missed` or `not_tested`. Calculate the percentage of expected telemetry observed and preserve the remediation owner.

### 4. Analyst validation
A detection result is not considered operationally validated simply because an alert fired. Analyst validation confirms that the evidence is attributable to the intended exercise, sufficiently contextualized and actionable.

### 5. Remediate
For gaps, improve data collection, parsing, detection logic, enrichment, alert routing, triage instructions or identity/network/endpoint controls as appropriate.

### 6. Retest
Any missed or partial detection should be re-exercised after remediation. A control is considered closed only after the revised detection is observed and analyst validation is complete.

## Risk model

Risk is intentionally explainable rather than predictive. It combines:

- business/security severity of the tested behavior;
- detection outcome;
- missing expected telemetry;
- absence of analyst validation.

Scores are capped at 100. ATT&CK mappings provide threat-behavior context and are not evidence of compromise.

## MITRE ATT&CK coverage

The synthetic dataset includes examples mapped to:

- T1059.001 — PowerShell;
- T1021.001 — Remote Desktop Protocol;
- T1562.001 — Impair Defenses;
- T1098 — Account Manipulation.

## Evidence standard

A credible validation record should retain:

- exercise identifier;
- approved technique/control objective;
- expected and observed telemetry;
- analytic outcome;
- analyst-validation state;
- accountable remediation owner;
- retest state;
- final validation evidence.

## Limitations

This lab does not connect to production SIEM, EDR, identity or network platforms. It does not run Atomic Red Team, CALDERA, C2 frameworks, exploit code, credential attacks or destructive tests. Real-world detections require environment-specific tuning and authorization.
