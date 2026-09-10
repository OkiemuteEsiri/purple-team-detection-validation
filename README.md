# Purple-Team Detection Validation

A recruiter-facing defensive security engineering project for measuring whether ATT&CK-aligned detections actually observe, alert on and support analyst investigation of controlled adversary-emulation scenarios.

The project focuses on **detection validation, telemetry coverage, analyst confirmation, remediation ownership and retesting**. It deliberately excludes live exploitation, offensive payloads and production targeting.

## Problem statement

Security teams often have detection rules mapped to MITRE ATT&CK but limited evidence that the rules work end to end. A rule can exist yet still fail because telemetry is missing, parsing is incomplete, enrichment is absent, routing is broken or the alert is not actionable.

This project models a disciplined purple-team validation workflow that answers:

- Was the expected telemetry collected?
- Did the analytic detect the controlled behavior?
- Was the alert validated by an analyst?
- What gap prevented complete detection?
- Who owns remediation?
- Is a retest required?
- Can the control be closed with evidence rather than assumption?

## Architecture

```text
Synthetic authorized exercise records
            |
            v
     Validated domain models
            |
            v
  Telemetry coverage calculation
            |
            v
 Detection-outcome assessment
            |
            v
 Explainable contextual risk score
            |
            +----> Portfolio metrics
            |
            +----> Markdown validation report
            |
            v
 Remediation -> retest -> analyst validation
```

## Repository structure

```text
.github/workflows/ci.yml          Least-privilege compile/test workflow
data/synthetic_exercises.json     Safe synthetic exercise observations
docs/architecture-methodology.md Architecture, methodology and closure criteria
reports/example-assessment.md     Example executive/analyst assessment
src/models.py                     Immutable validated domain models
src/engine.py                     Coverage, scoring, IDs and portfolio metrics
src/reporting.py                  Markdown report generation
tests/test_engine.py              Unit tests for validation behavior
README.md                         Recruiter-facing project documentation
```

## Implemented capabilities

- immutable purple-team exercise and validation-finding models;
- input validation for exercise IDs, ATT&CK technique format, severity and outcomes;
- deterministic SHA-256-derived finding IDs;
- expected-versus-observed telemetry coverage measurement;
- explicit outcomes: `detected`, `partial`, `missed`, `not_tested`;
- analyst-validation state kept separate from raw analytic outcome;
- explainable bounded 0–100 contextual risk scoring;
- remediation ownership and retest tracking;
- duplicate exercise-ID rejection during ingestion;
- portfolio metrics for validated controls, gaps, retests, coverage and mean risk;
- Markdown reporting for executive and analyst consumption;
- realistic synthetic ATT&CK-aligned exercise data;
- unit tests and least-privilege CI.

## ATT&CK coverage

The synthetic dataset demonstrates defensive validation around:

| Technique | Description | Validation focus |
|---|---|---|
| T1059.001 | PowerShell | Process and command-line telemetry |
| T1021.001 | Remote Desktop Protocol | Remote-logon correlation and context |
| T1562.001 | Impair Defenses | Endpoint control state-change telemetry |
| T1098 | Account Manipulation | Directory audit and privileged account changes |

ATT&CK mappings are used as threat-behavior context. They are **not evidence that compromise occurred**.

## Risk design

Risk scoring is intentionally transparent rather than machine-learned. It combines:

1. security severity of the tested behavior;
2. whether the detection was missed, partial or not tested;
3. the fraction of expected telemetry that was absent;
4. whether analyst validation remains incomplete.

The score is capped at 100. A complete alert with all expected telemetry and analyst confirmation produces lower residual risk than a high-severity behavior that is missed or lacks required telemetry.

## Validation lifecycle

```text
Plan authorized scenario
        ↓
Define expected telemetry and success criteria
        ↓
Run controlled/synthetic exercise outside this repository
        ↓
Collect representative observations
        ↓
Evaluate telemetry + analytic outcome
        ↓
Analyst validates evidence
        ↓
Gap? ── yes ──> Remediate ──> Retest
  │
  no
  ↓
Evidence-based closure
```

A detection rule is not treated as validated simply because it exists or fires once. Closure requires sufficient telemetry, intended analytic behavior and analyst-confirmed evidence.

## Example usage

From the repository root:

```python
from src.engine import assess, load_exercises
from src.reporting import render_markdown

exercises = load_exercises("data/synthetic_exercises.json")
findings = [assess(exercise) for exercise in exercises]
print(render_markdown(findings))
```

Run the unit suite with:

```bash
python -m unittest discover -s tests -v
```

## Testing strategy

The test suite covers:

- full and partial telemetry coverage;
- critical missed detections scoring above validated lower-risk controls;
- bounded risk scores;
- deterministic finding IDs;
- ATT&CK technique validation;
- invalid retest state rejection;
- portfolio metrics;
- duplicate exercise-ID rejection;
- report rendering and ATT&CK context.

Tests being present in the repository does not imply a successful run until CI or local execution is explicitly verified.

## Remediation and revalidation

Typical gap remediation can include:

- enabling or repairing telemetry collection;
- parser/schema normalization;
- enrichment with identity, host, asset or network context;
- detection-query tuning;
- improving alert severity and routing;
- adding triage guidance and evidence fields;
- control hardening when the exercise exposes a preventive-control weakness.

After remediation, the same authorized exercise should be repeated and the revised evidence reviewed by an analyst. A configuration change without a successful retest is not counted as validated closure.

## Skills demonstrated

This project demonstrates practical capability in:

- Purple Teaming
- Detection Engineering
- MITRE ATT&CK mapping
- Security control validation
- Incident-response readiness
- Telemetry quality analysis
- Risk-based prioritization
- Python security engineering
- Defensive data modeling
- Security metrics and reporting
- Test-driven validation
- CI/CD security hygiene

## Safety and ethics

This repository contains no exploit payloads, malware, persistence mechanisms, credential theft, C2 infrastructure, destructive actions or production targeting. The dataset is synthetic. Offensive behavior is represented only as ATT&CK-aligned control-validation context for authorized defensive testing.

## Limitations

- No live SIEM, EDR, IdP or network integrations are performed.
- Scores are prioritization aids, not proof of compromise or business-loss predictions.
- Synthetic telemetry cannot capture every vendor-specific schema or environmental dependency.
- Detection logic still requires tuning against an authorized target environment before production use.

## Roadmap

- add Sigma/KQL/Sentinel analytic metadata adapters;
- add detection-as-code validation against synthetic event fixtures;
- add ATT&CK coverage matrices by tactic and technique;
- add control-owner SLA and aging metrics;
- add false-positive/false-negative validation records;
- add evidence snapshots for before/after remediation comparison;
- add JSON and CSV report exporters;
- add optional mocked SIEM-provider adapters without live targeting.
