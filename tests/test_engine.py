import json
import tempfile
import unittest
from pathlib import Path

from src.engine import assess, load_exercises, portfolio_metrics
from src.models import Exercise
from src.reporting import render_markdown


def sample(**overrides):
    base = dict(
        exercise_id="PT-X",
        technique_id="T1059.001",
        technique_name="PowerShell",
        control_name="Synthetic analytic",
        severity="high",
        expected_telemetry=("a", "b"),
        observed_telemetry=("a", "b"),
        detection_outcome="detected",
        analyst_validated=True,
        remediation_owner="Detection Engineering",
        retest_required=False,
    )
    base.update(overrides)
    return Exercise(**base)


class EngineTests(unittest.TestCase):
    def test_full_coverage_is_one(self):
        self.assertEqual(assess(sample()).telemetry_coverage, 1.0)

    def test_partial_coverage(self):
        finding = assess(sample(observed_telemetry=("a",), detection_outcome="partial", retest_required=True))
        self.assertEqual(finding.telemetry_coverage, 0.5)

    def test_missed_critical_scores_higher_than_validated_high(self):
        good = assess(sample())
        bad = assess(sample(severity="critical", observed_telemetry=("a",), detection_outcome="missed", analyst_validated=False, retest_required=True))
        self.assertGreater(bad.risk_score, good.risk_score)

    def test_score_is_bounded(self):
        finding = assess(sample(severity="critical", observed_telemetry=(), detection_outcome="missed", analyst_validated=False, retest_required=True))
        self.assertLessEqual(finding.risk_score, 100)

    def test_finding_id_is_deterministic(self):
        self.assertEqual(assess(sample()).finding_id, assess(sample()).finding_id)

    def test_invalid_technique_rejected(self):
        with self.assertRaises(ValueError):
            sample(technique_id="bad")

    def test_validated_detection_cannot_require_retest(self):
        with self.assertRaises(ValueError):
            sample(retest_required=True)

    def test_portfolio_metrics(self):
        findings = [
            assess(sample(exercise_id="A")),
            assess(sample(exercise_id="B", observed_telemetry=("a",), detection_outcome="partial", retest_required=True)),
        ]
        metrics = portfolio_metrics(findings)
        self.assertEqual(metrics["total"], 2)
        self.assertEqual(metrics["gaps"], 1)
        self.assertEqual(metrics["retests"], 1)

    def test_duplicate_exercise_id_rejected(self):
        payload = [
            {
                "exercise_id":"DUP","technique_id":"T1098","technique_name":"Account Manipulation","control_name":"x","severity":"medium",
                "expected_telemetry":["a"],"observed_telemetry":["a"],"detection_outcome":"detected","analyst_validated":True,"remediation_owner":"IR","retest_required":False
            },
            {
                "exercise_id":"DUP","technique_id":"T1098","technique_name":"Account Manipulation","control_name":"y","severity":"medium",
                "expected_telemetry":["a"],"observed_telemetry":["a"],"detection_outcome":"detected","analyst_validated":True,"remediation_owner":"IR","retest_required":False
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_exercises(path)

    def test_report_contains_attack_and_retest(self):
        finding = assess(sample(exercise_id="R", observed_telemetry=("a",), detection_outcome="partial", retest_required=True))
        report = render_markdown([finding])
        self.assertIn("T1059.001", report)
        self.assertIn("Retests required: 1", report)


if __name__ == "__main__":
    unittest.main()
