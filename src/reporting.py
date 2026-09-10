from __future__ import annotations

from .engine import portfolio_metrics
from .models import ValidationFinding


def render_markdown(findings: list[ValidationFinding]) -> str:
    metrics = portfolio_metrics(findings)
    lines = [
        "# Purple-Team Detection Validation Report",
        "",
        "Synthetic, authorized validation data only.",
        "",
        "## Executive Metrics",
        f"- Total exercises: {metrics['total']}",
        f"- Fully validated: {metrics['validated']}",
        f"- Detection gaps: {metrics['gaps']}",
        f"- Retests required: {metrics['retests']}",
        f"- Mean telemetry coverage: {metrics['mean_coverage']:.0%}",
        f"- Mean contextual risk: {metrics['mean_risk']}",
        "",
        "## Findings",
        "",
        "| Exercise | ATT&CK | Outcome | Coverage | Risk | Owner | Retest |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for f in sorted(findings, key=lambda x: x.risk_score, reverse=True):
        lines.append(
            f"| {f.exercise_id} | {f.technique_id} | {f.outcome} | {f.telemetry_coverage:.0%} | "
            f"{f.risk_score} | {f.remediation_owner or 'unassigned'} | {'yes' if f.retest_required else 'no'} |"
        )
    lines.extend(["", "## Analyst Notes", ""])
    for f in sorted(findings, key=lambda x: x.risk_score, reverse=True):
        lines.append(f"### {f.finding_id} — {f.exercise_id}")
        lines.append(f"{f.gap_summary}")
        lines.append("")
    return "\n".join(lines)
