from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

from .models import Exercise, ValidationFinding

SEVERITY_WEIGHT = {"low": 15, "medium": 35, "high": 60, "critical": 80}
OUTCOME_WEIGHT = {"detected": 0, "partial": 15, "missed": 20, "not_tested": 10}


def _coverage(exercise: Exercise) -> float:
    expected = set(exercise.expected_telemetry)
    observed = set(exercise.observed_telemetry)
    return round(len(expected & observed) / len(expected), 2)


def _finding_id(exercise: Exercise) -> str:
    raw = f"{exercise.exercise_id}|{exercise.technique_id}|{exercise.control_name}".encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def assess(exercise: Exercise) -> ValidationFinding:
    coverage = _coverage(exercise)
    score = SEVERITY_WEIGHT[exercise.severity] + OUTCOME_WEIGHT[exercise.detection_outcome]
    score += round((1 - coverage) * 20)
    if not exercise.analyst_validated:
        score += 10
    score = max(0, min(100, score))

    missing = sorted(set(exercise.expected_telemetry) - set(exercise.observed_telemetry))
    if exercise.detection_outcome == "detected" and exercise.analyst_validated and coverage == 1:
        summary = "Detection validated with complete expected telemetry."
    else:
        detail = ", ".join(missing) if missing else "none"
        summary = f"Validation gap: outcome={exercise.detection_outcome}; missing telemetry={detail}."

    return ValidationFinding(
        finding_id=_finding_id(exercise),
        exercise_id=exercise.exercise_id,
        technique_id=exercise.technique_id,
        severity=exercise.severity,
        outcome=exercise.detection_outcome,
        telemetry_coverage=coverage,
        risk_score=score,
        gap_summary=summary,
        remediation_owner=exercise.remediation_owner,
        retest_required=exercise.retest_required,
    )


def portfolio_metrics(findings: list[ValidationFinding]) -> dict:
    if not findings:
        return {"total": 0, "validated": 0, "gaps": 0, "retests": 0, "mean_coverage": 0.0, "mean_risk": 0.0}
    validated = sum(f.outcome == "detected" and f.telemetry_coverage == 1 for f in findings)
    gaps = sum(f.outcome in {"missed", "partial"} for f in findings)
    return {
        "total": len(findings),
        "validated": validated,
        "gaps": gaps,
        "retests": sum(f.retest_required for f in findings),
        "mean_coverage": round(mean(f.telemetry_coverage for f in findings), 2),
        "mean_risk": round(mean(f.risk_score for f in findings), 1),
    }


def load_exercises(path: str | Path) -> list[Exercise]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    seen: set[str] = set()
    exercises: list[Exercise] = []
    for item in data:
        if item["exercise_id"] in seen:
            raise ValueError(f"duplicate exercise_id: {item['exercise_id']}")
        seen.add(item["exercise_id"])
        exercises.append(Exercise(
            exercise_id=item["exercise_id"],
            technique_id=item["technique_id"],
            technique_name=item["technique_name"],
            control_name=item["control_name"],
            severity=item["severity"],
            expected_telemetry=tuple(item["expected_telemetry"]),
            observed_telemetry=tuple(item["observed_telemetry"]),
            detection_outcome=item["detection_outcome"],
            analyst_validated=bool(item["analyst_validated"]),
            remediation_owner=item["remediation_owner"],
            retest_required=bool(item["retest_required"]),
        ))
    return exercises
