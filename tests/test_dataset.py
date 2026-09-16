from __future__ import annotations

import csv
import json
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reference_engine import FIELDS, authorize, evidence_ids_for, recommend  # noqa: E402


def rows(name: str) -> list[dict]:
    with (ROOT / "data" / name).open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "src" / "generate_dataset.py")], check=True, cwd=ROOT)

    def test_profile_cardinality_and_uniqueness(self) -> None:
        base = rows("evidence_profiles.csv")
        conflicts = rows("conflict_profiles.csv")
        self.assertEqual(len(base), 81)
        self.assertEqual(len(conflicts), 81)
        self.assertEqual(len({row["profile_id"] for row in base + conflicts}), 162)

    def test_base_label_distribution(self) -> None:
        counts = Counter(row["expected_label"] for row in rows("evidence_profiles.csv"))
        self.assertEqual(
            counts,
            {
                "conceptual": 27,
                "representational": 9,
                "instrumental": 3,
                "implementation": 1,
                "no_observed_barrier": 1,
                "insufficient": 40,
            },
        )

    def test_conflict_override(self) -> None:
        for row in rows("conflict_profiles.csv"):
            self.assertEqual(row["expected_rule"], "R0")
            self.assertEqual(row["expected_label"], "review")

    def test_missing_evidence_is_not_failure(self) -> None:
        values = dict(zip(FIELDS, ("pass", "unknown", "fail", "fail")))
        result = recommend(values, evidence_ids_for(values))
        self.assertEqual(result.label, "insufficient")
        self.assertEqual(result.rule, "RU")

    def test_observed_state_requires_identifier(self) -> None:
        values = dict(zip(FIELDS, ("pass", "pass", "pass", "pass")))
        evidence = evidence_ids_for(values)
        evidence["reasoning"] = None
        with self.assertRaises(ValueError):
            recommend(values, evidence)

    def test_teacher_decision_does_not_mutate_proposal(self) -> None:
        values = dict(zip(FIELDS, ("pass", "pass", "fail", "fail")))
        proposal = recommend(values, evidence_ids_for(values))
        accepted = authorize(proposal, "accept", "constructed-teacher", "constructed example")
        rejected = authorize(proposal, "reject", "constructed-teacher", "constructed example")
        postponed = authorize(proposal, "postpone", "constructed-teacher", "constructed example")
        self.assertTrue(accepted["applied"])
        self.assertFalse(rejected["applied"])
        self.assertFalse(postponed["applied"])
        self.assertFalse(proposal.applied)
        self.assertEqual(proposal.teacher_status, "pending")

    def test_manifest_scope(self) -> None:
        manifest = json.loads((ROOT / "metadata" / "manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["contains_participant_data"])
        self.assertTrue(manifest["deterministic"])
        self.assertEqual(manifest["version"], "1.0.0")


if __name__ == "__main__":
    unittest.main(verbosity=2)

