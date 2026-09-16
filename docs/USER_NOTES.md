# User notes

## Loading the benchmark

The files use UTF-8 encoding, comma delimiters, and Unix line endings.

```python
import csv

with open("data/expected_recommendations.csv", encoding="utf-8", newline="") as stream:
    profiles = list(csv.DictReader(stream))

print(len(profiles))  # 162
```

Boolean values are serialized as lowercase `true` and `false`. The
`evidence_ids` column contains a JSON array encoded inside the CSV field.

## Recommended comparison protocol

1. Load the 162 benchmark cases.
2. Submit the four evidence states and the conflict flag to the implementation.
3. Compare rule, label, evidence use, action, authorization state, and applied state.
4. Report mismatches by `profile_id`.
5. Keep any implementation-specific confidence separate from the benchmark;
   the released outputs are not probabilistically calibrated.

## Extending the dataset

Additional expert or classroom cases should be stored separately from the
constructed benchmark. Each new record should state its source, coder,
instrument, version, consent/ethics basis where applicable, and relationship to
the original evidence artifact. Do not overwrite the v1.0.0 benchmark cases.

