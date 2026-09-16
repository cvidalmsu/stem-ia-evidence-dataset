# Dataset construction methods

## Scope

The dataset operationalizes a narrow evidence-to-action boundary for STEM-IA
Escolar. It does not implement automated artifact analysis, train an artificial
intelligence model, or reproduce a classroom intervention.

## Profile generation

Four ordered evidence dimensions are represented: reasoning, representation,
operation, and execution. Each dimension admits three states (`pass`, `fail`,
and `unknown`). The generator enumerates the complete Cartesian product,
yielding 3^4 = 81 base profiles.

For every base profile, a corresponding case is created with an explicit
conflict flag. These 81 additional cases test whether contradictory evidence is
routed to teacher review before any ordinary rule is applied.

## Rule semantics

The standard rules follow a prerequisite-prefix ordering. The first unresolved
or failed prerequisite determines the provisional support category. Missing
evidence causes abstention (`insufficient`), while explicit conflict has the
highest priority (`review`). All proposed actions remain pending until a teacher
accepts, rejects, or postpones them.

## Reproducibility

`src/generate_dataset.py` is the authoritative generator. It produces the CSV
tables, manifest, and checksums using only the Python standard library.
`tests/test_dataset.py` verifies cardinality, label distribution, conflict
override, evidence identifiers, missing-evidence behavior, teacher-decision
invariants, and the non-participant scope of the package.

## Interpretation boundary

Conformance with these rules is not evidence of diagnostic correctness. The
rule order, curriculum mapping, labels, wording of actions, and teacher
interaction require prospective validation by experts and users.

