from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

VALID_OUTCOMES = {"detected", "missed", "partial", "not_tested"}
VALID_SEVERITIES = {"low", "medium", "high", "critical"}


@dataclass(frozen=True)
class Exercise:
    exercise_id: str
    technique_id: str
    technique_name: str
    control_name: str
    severity: str
    expected_telemetry: Tuple[str, ...]
    observed_telemetry: Tuple[str, ...]
    detection_outcome: str
    analyst_validated: bool
    remediation_owner: str
    retest_required: bool

    def __post_init__(self) -> None:
        if not self.exercise_id.strip():
            raise ValueError("exercise_id is required")
        if not self.technique_id.startswith("T"):
            raise ValueError("technique_id must look like a MITRE ATT&CK technique")
        if self.severity not in VALID_SEVERITIES:
            raise ValueError(f"unsupported severity: {self.severity}")
        if self.detection_outcome not in VALID_OUTCOMES:
            raise ValueError(f"unsupported outcome: {self.detection_outcome}")
        if not self.expected_telemetry:
            raise ValueError("expected_telemetry cannot be empty")
        if self.retest_required and self.detection_outcome == "detected" and self.analyst_validated:
            raise ValueError("validated detections should not require retest")


@dataclass(frozen=True)
class ValidationFinding:
    finding_id: str
    exercise_id: str
    technique_id: str
    severity: str
    outcome: str
    telemetry_coverage: float
    risk_score: int
    gap_summary: str
    remediation_owner: str
    retest_required: bool
