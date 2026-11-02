# Astro Membrane Simulation

A standard-library-only Python research prototype containing four independent synthetic simulation lanes:

- Holographic boundary compression
- Anti-crystallization phase monitoring
- Relativistic synchronization prediction
- Self-calibration verification

This is a synthetic demonstration only. It does not control spacecraft, connect to orbital sensors, or replace flight-certified navigation software.

## Run

```bash
python3 astro_membrane_sim.py --seed 7 --report sample_astro_report.json
```

The runtime timestamp is intentionally excluded from the report. Identical seeds therefore produce byte-for-byte identical reports and deterministic SHA-256 values.

## Orbital phase-field engine

`orbital_phase_field_engine.py` adds a synthetic phase-field testbench with:

- A double-well potential, gradient term, and crystallization penalty
- Fail-closed validation for phase bounds, non-negative terms, finite values, and configuration ranges
- An explicit reachable phase-lock threshold; the previous `double_well > 0.15` condition was removed because the potential's maximum on `[0, 1]` is `1/16`
- A private seeded RNG so simulations do not consume or mutate global random state
- Timestamp-free canonical JSON reports with deterministic SHA-256 digests

Run it with:

```bash
python3 orbital_phase_field_engine.py \
  --seed 42 \
  --steps 5 \
  --output phase_field_audit_report.json
```

Run the regression suite with:

```bash
python3 -m unittest -v test_orbital_phase_field_engine.py
```

All models in this repository are synthetic research prototypes. They do not control spacecraft, active manufacturing machinery, or other physical systems, and they are not flight-certified scientific software.

## Unified master engine

`sparkainlp_master_engine.py` composes the four lanes into one deterministic audit:

1. Bulk-to-boundary membrane summaries
2. Validated phase-field free energy and anti-crystallization status
3. Lagged telemetry prediction
4. Invariant-based calibration checks

The master engine uses the hardened phase-field implementation, a private seeded RNG, strict finite-value validation, equal-length checks for telemetry vectors, and canonical timestamp-free JSON hashing.

Run the master audit with:

```bash
python3 sparkainlp_master_engine.py \
  --seed 42 \
  --output master_audit_report.json
```

Run all tests with:

```bash
python3 -m unittest -v test_orbital_phase_field_engine.py test_master_engine.py
```

A Zenodo DOI or other archival identifier must only be added after an actual archive deposit and verification; the repository does not claim one automatically.
