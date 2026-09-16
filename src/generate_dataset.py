"""Generate every released table, manifest, and checksum deterministically."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from reference_engine import ACTIONS, FIELDS, LABELS, STATES, evidence_ids_for, recommend


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
METADATA = ROOT / "metadata"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def profile_rows(conflict: bool) -> list[dict]:
    rows = []
    prefix = "C" if conflict else "P"
    for index, states in enumerate(itertools.product(STATES, repeat=4), start=1):
        values = dict(zip(FIELDS, states))
        evidence_ids = evidence_ids_for(values)
        result = recommend(values, evidence_ids, conflict=conflict)
        rows.append(
            {
                "profile_id": f"{prefix}{index:03d}",
                **values,
                "conflict": str(conflict).lower(),
                "expected_rule": result.rule,
                "expected_label": result.label,
                "expected_action": result.action,
                "evidence_ids": json.dumps(result.evidence, ensure_ascii=False),
                "evidence_count": len(result.evidence),
                "uncertainty": result.uncertainty,
                "teacher_status": result.teacher_status,
                "applied": str(result.applied).lower(),
                "data_origin": "deterministically_constructed",
                "participant_data": "false",
            }
        )
    return rows


def static_tables() -> None:
    rules = [
        {"rule_id": "R0", "priority": 0, "trigger": "conflict=true", "label": "review", "action": ACTIONS["review"]},
        {"rule_id": "RU", "priority": 1, "trigger": "first required state is unknown", "label": "insufficient", "action": ACTIONS["insufficient"]},
        {"rule_id": "R1", "priority": 2, "trigger": "reasoning=fail", "label": LABELS[0], "action": ACTIONS[LABELS[0]]},
        {"rule_id": "R2", "priority": 3, "trigger": "reasoning=pass and representation=fail", "label": LABELS[1], "action": ACTIONS[LABELS[1]]},
        {"rule_id": "R3", "priority": 4, "trigger": "reasoning=pass and representation=pass and operation=fail", "label": LABELS[2], "action": ACTIONS[LABELS[2]]},
        {"rule_id": "R4", "priority": 5, "trigger": "reasoning=pass and representation=pass and operation=pass and execution=fail", "label": LABELS[3], "action": ACTIONS[LABELS[3]]},
        {"rule_id": "R5", "priority": 6, "trigger": "all four states=pass", "label": "no_observed_barrier", "action": ACTIONS["no_observed_barrier"]},
    ]
    write_csv(DATA / "recommendation_rules.csv", list(rules[0]), rules)

    competencies = [
        {"domain_id": "D1", "domain": "problem_formulation", "observable_performance": "Identifies purpose, users, variables, constraints and success criteria", "representative_evidence": "problem statement; annotated variables; success criteria"},
        {"domain_id": "D2", "domain": "algorithm_design", "observable_performance": "Decomposes the problem and specifies ordered procedures", "representative_evidence": "unplugged trace; pseudocode; flow diagram"},
        {"domain_id": "D3", "domain": "block_programming", "observable_performance": "Implements sequences, conditions, iteration and variables", "representative_evidence": "Scratch project; execution trace; explanation"},
        {"domain_id": "D4", "domain": "electronic_simulation", "observable_performance": "Connects code, sensors, actuators and simulated circuit behavior", "representative_evidence": "Tinkercad circuit; simulation log; annotated connections"},
        {"domain_id": "D5", "domain": "physical_computing", "observable_performance": "Builds and tests an Arduino-compatible physical prototype", "representative_evidence": "prototype; code; calibration and debugging record"},
        {"domain_id": "D6", "domain": "data_and_scientific_reasoning", "observable_performance": "Measures, represents and interprets data from the designed system", "representative_evidence": "measurement table; graph; evidence-based explanation"},
        {"domain_id": "D7", "domain": "evaluation_and_communication", "observable_performance": "Evaluates the solution against criteria and communicates limitations", "representative_evidence": "test results; revision log; presentation; reflection"},
    ]
    write_csv(DATA / "competency_evidence_model.csv", list(competencies[0]), competencies)

    mappings = [
        {"mapping_id": "M01", "curriculum_area": "Technology", "grade_band": "7-8 basic education", "learning_focus": "Identify needs and define technological problems", "dataset_domain_id": "D1", "mapping_status": "design_mapping_requires_expert_validation"},
        {"mapping_id": "M02", "curriculum_area": "Technology", "grade_band": "7-8 basic education", "learning_focus": "Design, implement and evaluate technological solutions", "dataset_domain_id": "D4;D5;D7", "mapping_status": "design_mapping_requires_expert_validation"},
        {"mapping_id": "M03", "curriculum_area": "Mathematics", "grade_band": "7-8 basic education", "learning_focus": "Variables, patterns, proportional reasoning and functions", "dataset_domain_id": "D2;D3;D6", "mapping_status": "design_mapping_requires_expert_validation"},
        {"mapping_id": "M04", "curriculum_area": "Mathematics", "grade_band": "7-8 basic education", "learning_focus": "Data representation and interpretation", "dataset_domain_id": "D6", "mapping_status": "design_mapping_requires_expert_validation"},
        {"mapping_id": "M05", "curriculum_area": "Natural Sciences", "grade_band": "7-8 basic education", "learning_focus": "Measurement, experimentation and interpretation of phenomena", "dataset_domain_id": "D4;D5;D6", "mapping_status": "design_mapping_requires_expert_validation"},
        {"mapping_id": "M06", "curriculum_area": "Cross-curricular STEM", "grade_band": "7-8 basic education", "learning_focus": "Integrate algorithms, models, evidence and technological design", "dataset_domain_id": "D1;D2;D3;D4;D5;D6;D7", "mapping_status": "design_mapping_requires_expert_validation"},
    ]
    write_csv(DATA / "curriculum_domain_mapping.csv", list(mappings[0]), mappings)


def dictionary_rows() -> list[dict]:
    descriptions = {
        "profile_id": ("string", "Unique constructed profile identifier"),
        "reasoning": ("categorical", "Algorithmic-reasoning evidence state"),
        "representation": ("categorical", "Block, diagram or symbolic representation evidence state"),
        "operation": ("categorical", "Tool-operation evidence state"),
        "execution": ("categorical", "Implementation or execution evidence state"),
        "conflict": ("boolean", "Whether explicit contradictory evidence overrides the standard rules"),
        "expected_rule": ("categorical", "Identifier of the rule expected to fire"),
        "expected_label": ("categorical", "Expected barrier or review label"),
        "expected_action": ("string", "Candidate teacher-facing support action"),
        "evidence_ids": ("JSON array", "Identifiers of constructed evidence used by the rule"),
        "evidence_count": ("integer", "Number of evidence identifiers used"),
        "uncertainty": ("categorical", "Calibration limitation of the deterministic result"),
        "teacher_status": ("categorical", "Authorization state before a teacher decision"),
        "applied": ("boolean", "Whether an action has been authorized and applied"),
        "data_origin": ("categorical", "Origin classification for the record"),
        "participant_data": ("boolean", "Whether the record contains participant observations"),
    }
    rows = []
    for dataset in ("evidence_profiles.csv", "conflict_profiles.csv", "expected_recommendations.csv"):
        for variable, (data_type, description) in descriptions.items():
            allowed = ""
            if variable in FIELDS:
                allowed = "pass|fail|unknown"
            elif variable == "expected_rule":
                allowed = "R0|RU|R1|R2|R3|R4|R5"
            elif variable == "expected_label":
                allowed = "review|insufficient|conceptual|representational|instrumental|implementation|no_observed_barrier"
            elif variable == "teacher_status":
                allowed = "pending"
            elif variable in ("conflict", "applied", "participant_data"):
                allowed = "true|false"
            rows.append({"dataset": dataset, "variable": variable, "data_type": data_type, "allowed_values": allowed, "description": description})
    return rows


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest() -> None:
    released = sorted(DATA.glob("*.csv")) + [METADATA / "data_dictionary.csv", METADATA / "schema.json"]
    resources = []
    for path in released:
        entry = {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if path.suffix == ".csv":
            with path.open("r", encoding="utf-8", newline="") as stream:
                entry["records"] = sum(1 for _ in csv.DictReader(stream))
        resources.append(entry)
    manifest = {
        "dataset": "STEM-IA Escolar curriculum-aligned evidence profiles",
        "version": "1.0.0",
        "generated_by": "src/generate_dataset.py",
        "deterministic": True,
        "contains_participant_data": False,
        "resources": resources,
    }
    (METADATA / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checksum_files = sorted(DATA.glob("*.csv")) + sorted(METADATA.glob("*.csv")) + sorted(METADATA.glob("*.json"))
    lines = [f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in checksum_files if path.name != "checksums_sha256.txt"]
    (METADATA / "checksums_sha256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    METADATA.mkdir(parents=True, exist_ok=True)
    base = profile_rows(conflict=False)
    conflict = profile_rows(conflict=True)
    fields = list(base[0])
    write_csv(DATA / "evidence_profiles.csv", fields, base)
    write_csv(DATA / "conflict_profiles.csv", fields, conflict)
    write_csv(DATA / "expected_recommendations.csv", fields, base + conflict)
    static_tables()
    write_csv(METADATA / "data_dictionary.csv", ["dataset", "variable", "data_type", "allowed_values", "description"], dictionary_rows())
    build_manifest()
    counts = Counter(row["expected_label"] for row in base)
    print(json.dumps({"base_profiles": len(base), "conflict_profiles": len(conflict), "base_label_counts": dict(counts)}, indent=2))


if __name__ == "__main__":
    main()

