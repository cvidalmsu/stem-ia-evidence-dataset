"""Deterministic reference specification for the STEM-IA evidence dataset.

The inputs are constructed evidence states, not observations of students.
No machine-learning model is trained or evaluated by this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


FIELDS = ("reasoning", "representation", "operation", "execution")
STATES = ("pass", "fail", "unknown")
LABELS = ("conceptual", "representational", "instrumental", "implementation")
ACTIONS = {
    "conceptual": "Request an unplugged tracing explanation",
    "representational": "Map the explained procedure to blocks or a diagram",
    "instrumental": "Provide a tool-navigation worked example",
    "implementation": "Inspect wiring, calibration, timing and tests",
    "no_observed_barrier": "Offer a teacher-selected transfer task",
    "insufficient": "Collect the missing prerequisite evidence",
    "review": "Ask the teacher to reconcile conflicting evidence",
}


@dataclass(frozen=True)
class Recommendation:
    version: str
    rule: str
    label: str
    evidence: tuple[str, ...]
    action: str
    uncertainty: str = "not_probabilistically_calibrated"
    teacher_status: str = "pending"
    applied: bool = False

    def to_dict(self) -> dict:
        result = asdict(self)
        result["evidence"] = list(self.evidence)
        return result


def evidence_ids_for(values: Mapping[str, str]) -> dict[str, str | None]:
    """Create deterministic identifiers for the constructed observations."""
    return {
        field: f"constructed-{field}" if values[field] != "unknown" else None
        for field in FIELDS
    }


def recommend(
    values: Mapping[str, str],
    evidence_ids: Mapping[str, str | None],
    conflict: bool = False,
) -> Recommendation:
    """Apply the declared prerequisite-prefix decision rules."""
    if set(values) != set(FIELDS) or set(evidence_ids) != set(FIELDS):
        raise ValueError("Exactly four evidence fields are required")

    for field in FIELDS:
        if values[field] not in STATES:
            raise ValueError(f"Invalid evidence state for {field}")
        if values[field] != "unknown" and not evidence_ids[field]:
            raise ValueError("Observed states require evidence identifiers")

    used: list[str] = []
    rule = "R5"
    label = "no_observed_barrier"

    if conflict:
        rule, label = "R0", "review"
        used = [
            str(evidence_ids[field])
            for field in FIELDS
            if values[field] != "unknown"
        ]
    else:
        for index, field in enumerate(FIELDS):
            if values[field] == "unknown":
                rule, label = "RU", "insufficient"
                break
            used.append(str(evidence_ids[field]))
            if values[field] == "fail":
                rule, label = f"R{index + 1}", LABELS[index]
                break

    return Recommendation(
        version="1.0.0",
        rule=rule,
        label=label,
        evidence=tuple(used),
        action=ACTIONS[label],
    )


def authorize(
    recommendation: Recommendation,
    decision: str,
    teacher_id: str,
    rationale: str,
) -> dict:
    """Return an auditable example decision without mutating the proposal."""
    if decision not in ("accept", "reject", "postpone"):
        raise ValueError("Unsupported teacher decision")
    if not teacher_id or not rationale:
        raise ValueError("Teacher identity and rationale are required")
    result = recommendation.to_dict()
    result.update(
        teacher_status=decision,
        teacher_id=teacher_id,
        rationale=rationale,
        applied=(decision == "accept"),
    )
    return result

