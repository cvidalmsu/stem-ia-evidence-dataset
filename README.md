# STEM-IA Escolar Evidence Profiles Dataset

[![Data license: CC BY 4.0](https://img.shields.io/badge/data%20license-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue.svg)](LICENSE-CODE)
[![Validation](https://github.com/cvidalmsu/stem-ia-evidence-dataset/actions/workflows/validate.yml/badge.svg)](https://github.com/cvidalmsu/stem-ia-evidence-dataset/actions/workflows/validate.yml)

Version 1.0.0

This repository contains a reproducible dataset of curriculum-aligned evidence
profiles and expected outputs for teacher-controlled algorithmic-thinking
support in Chilean seventh- and eighth-grade basic education.

The records are **deterministically constructed test profiles**. They are not
student observations, diagnoses, assessments, or simulated individuals. No
personal or participant-level data are included.

## Released resources

| Resource | Records | Purpose |
|---|---:|---|
| `data/evidence_profiles.csv` | 81 | Exhaustive `pass`/`fail`/`unknown` combinations for four evidence dimensions. |
| `data/conflict_profiles.csv` | 81 | The same profiles with an explicit conflict requiring teacher review. |
| `data/expected_recommendations.csv` | 162 | Combined benchmark with expected rules, labels, evidence links, and actions. |
| `data/recommendation_rules.csv` | 7 | Human-readable rule catalog. |
| `data/competency_evidence_model.csv` | 7 | Competency domains, observable performance, and representative evidence. |
| `data/curriculum_domain_mapping.csv` | 6 | Design mapping across Technology, Mathematics, Natural Sciences, and STEM. |

The base profiles produce the following exhaustive label distribution:

- conceptual: 27;
- representational: 9;
- instrumental: 3;
- implementation: 1;
- no observed barrier: 1; and
- insufficient evidence: 40.

All 81 conflict variants produce `review` under rule `R0`.

## Evidence dimensions

1. `reasoning`: algorithmic reasoning demonstrated independently of a tool;
2. `representation`: mapping the procedure to blocks, diagrams, or another representation;
3. `operation`: operating Scratch, Tinkercad, or the relevant interface; and
4. `execution`: executing or implementing the digital, simulated, or physical artifact.

Each dimension uses `pass`, `fail`, or `unknown`. `unknown` is preserved as
missing prerequisite evidence and is never silently converted to failure.

## Reproduce the release

Python 3.10 or newer is sufficient. The release has no third-party runtime
dependencies.

```bash
python src/generate_dataset.py
python -m unittest discover -s tests -v
```

Expected final line:

```text
OK
```

The generation command rewrites the released CSV tables, the machine-readable
manifest, and SHA-256 checksums deterministically.

## Repository organization

```text
data/       Released CSV resources
metadata/   Dictionary, schema, provenance, manifest, and checksums
src/        Reference rule engine and deterministic generator
tests/      Conformance and integrity tests
examples/   Minimal machine-readable use examples
docs/       Methods, user notes, limitations, and publication instructions
```

## Intended uses

- unit and regression testing of educational decision-support prototypes;
- teaching examples for evidence provenance and abstention;
- comparison of rule-based implementations against a declared oracle;
- interface prototyping for teacher inspection, correction, and authorization;
- extension with expert-validated cases while retaining provenance; and
- reproducibility demonstrations for curriculum-aligned learning analytics.

## Inappropriate uses

The dataset must not be used to diagnose, grade, rank, label, or make high-stakes
decisions about learners. It does not establish diagnostic validity, educational
effectiveness, fairness, usability, or generalization to classroom evidence.
The curriculum mapping is a design artifact that still requires prospective
review by Chilean teachers and subject-matter experts.

## Citation

Please cite the archived Version 1.0.0:

Vidal-Silva, C., et al. (2026). STEM-IA Escolar: A Reproducible
Dataset of Curriculum-Aligned Evidence Profiles and Teacher-Controlled
Recommendation Rules (Version 1.0.0) [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.XXXXXXXX

## Licenses

- Data, metadata, and documentation: [CC BY 4.0](LICENSE).
- Source code and tests: [MIT](LICENSE-CODE).

## Contact

Cristian Vidal-Silva, Universidad de Talca, Chile: `cvidal@utalca.cl`.

