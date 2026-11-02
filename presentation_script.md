# Astro Membrane Simulation
## Architecture and Deterministic Design — Presentation Script

### Opening

Good morning. This presentation introduces `astro_membrane_sim.py`, a standard-library-only Python research prototype that combines four independent simulation lanes into one reproducible reporting pipeline.

The important qualification is that this is a synthetic demonstration. It does not connect to spacecraft, orbital sensors, or flight systems, and it does not make astrophysical claims. The value of the prototype is architectural: it demonstrates how separate analytical concepts can be isolated, executed, and reported consistently in an offline environment.

---

## Slide 1 — System Overview

The system has three layers.

At the input layer, the program creates synthetic bulk data, velocity vectors, and sensor readings. These inputs are generated locally and require no network connection or external hardware.

At the processing layer, four independent components analyze the inputs. Each component has a narrow responsibility and no hidden shared state with the others.

At the reporting layer, the results are assembled into a JSON document. The document is written to disk and assigned a deterministic SHA-256 digest so that another run with the same seed can be compared directly.

The overall flow is:

```text
seeded synthetic inputs
          |
          v
+-----------------------------+
| Four independent lanes      |
|                             |
| 1. Boundary mapper          |
| 2. Crystallization guard    |
| 3. Relativistic sync        |
| 4. Self-calibrator          |
+-----------------------------+
          |
          v
 deterministic JSON report
          |
          v
      SHA-256 digest
```

---

## Slide 2 — Lane 1: Holographic Boundary Mapper

The first lane is implemented by `HolographicBoundaryMapper`.

It accepts a flat synthetic bulk-volume vector and divides it into fixed-width cells. For each cell, it computes two summary values: the root-mean-square energy and the maximum observed value, or peak anomaly.

In the default simulation, 64 values are divided into two cells of 32 values each. The output is therefore a compact boundary representation rather than the original full vector.

This is an engineering abstraction inspired by boundary-projection terminology. It should be understood as a classical numerical compression operation, not as an implementation or validation of holographic physics.

The key architectural property is isolation: this mapper transforms its input and returns structured output without modifying global state.

---

## Slide 3 — Lane 2: Anti-Crystallization Guard

The second lane is implemented by `AntiCrystallizationGuard`.

It receives a phase-order parameter and a crystallization index. The residual is calculated as the absolute difference between the phase-order parameter and the target value of one.

The guard marks the state as locked when either the crystallization index exceeds the configured tolerance or the residual exceeds that tolerance. Otherwise, it reports a fluid-adaptive state.

For the sample run, the phase-order parameter is 0.82, producing a residual of 0.18. With a tolerance of 0.25 and a crystallization index of 0.15, the lane returns `FLUID_ADAPTIVE`.

This component is a threshold-based decision model. It does not physically damp a material or control a system; the `DAMPING_APPLIED` value is a simulation status label.

---

## Slide 4 — Lane 3: Relativistic Synchronization Engine

The third lane is implemented by `RelativisticSyncEngine`.

The purpose of this lane is to model predictive state estimation when communication includes a fixed delay. For each telemetry value, the engine adds a drift term calculated from the corresponding velocity and the sum of elapsed ticks and configured light-lag seconds.

In the sample configuration, the simulated lag is 1.5 seconds and the elapsed tick count is three. The engine predicts a future or delayed state for the telemetry sample.

This is a simple linear extrapolation model. It is not a relativistic physics engine, a navigation system, or a substitute for flight-certified synchronization software.

As with the other lanes, it is deterministic because the inputs, arithmetic operations, and configuration are fixed for a given seed.

---

## Slide 5 — Lane 4: Self-Knowing Calibrator

The fourth lane is implemented by `SelfKnowingCalibrator`.

It validates each sensor reading against two basic conditions: the reading must be positive, and its lower uncertainty bound must also be positive.

It then calculates the mean telemetry value and measures its absolute drift from the configured invariant target. Calibration is reported as `LOCKED` only when all samples are admissible and the drift is below 0.05.

For the sample readings—1.002, 0.998, 1.001, and 1.004—the mean is 1.00125, the invariant drift is approximately 0.00125, and the status is `LOCKED`.

The term “self-knowing” describes the internal verification pattern used by the prototype. It does not imply consciousness, autonomous authority, or a validated physical conservation law.

---

## Slide 6 — Separation of Lanes

A central design decision is the separation of the four lanes.

Each class owns its configuration and exposes a focused method. The simulation driver constructs the components, passes explicit inputs, and collects explicit return values.

There is no shared mutable telemetry store, no hidden cross-lane feedback loop, and no network dependency. This makes the prototype easier to test, reason about, and replace one component at a time.

This separation also limits the meaning of each result. A status from the anti-crystallization guard cannot silently alter the synchronization prediction, and the calibration result cannot modify the boundary mapper.

The architecture is therefore modular even though the final report presents the results together.

---

## Slide 7 — Seeded Synthetic Inputs

Reproducibility begins in `run_simulation`.

The function calls `random.seed(seed)` before generating any random values. The bulk data contains 64 uniformly distributed values between 0.1 and 0.9. A matching set of 64 velocity values is generated between -0.02 and 0.02.

The sensor readings and simulation parameters are explicit constants. There are no calls to external sensors, system entropy, network services, or current time during simulation.

As a result, the same seed produces the same synthetic input vectors, which produce the same lane outputs.

For example:

```bash
python3 astro_membrane_sim.py --seed 7 --report sample_astro_report.json
```

---

## Slide 8 — The Timestamp Determinism Fix

The original prototype included a runtime UTC timestamp in the report. That made two otherwise identical executions differ, because the timestamp changed between runs.

The updated design intentionally excludes runtime timestamps from the report. This is the simplest and clearest solution when byte-for-byte reproducibility is required.

The report metadata now records the generator, version, seed, synthetic-data designation, and the fact that the runtime timestamp was excluded. None of these values changes between runs with the same configuration.

If operational timing is needed in a future version, it should be stored separately from the deterministic artifact or explicitly excluded from the hashed payload.

---

## Slide 9 — Canonical JSON and SHA-256

The script uses a `canonical_json_bytes` helper to create a stable byte representation before hashing.

It applies three rules:

1. Dictionary keys are sorted with `sort_keys=True`.
2. Whitespace is minimized with compact separators.
3. UTF-8 encoding is used consistently.

The deterministic digest is calculated with SHA-256 over the report content before the digest field is added. The resulting digest is then stored in `metadata.deterministic_sha256`.

This avoids a self-referential hash problem: the hash does not include itself.

The command prints the digest, and the JSON report contains the same value. This gives both a quick terminal check and a durable provenance value inside the artifact.

---

## Slide 10 — Verification Result

The updated script was executed twice with seed 7.

Both runs produced the same complete report file SHA-256:

```text
e94b48e796e8e3c7a9feb56e0d5ce3f0245e80b533d9c0c3e2026ea1a6855370
```

Both runs also reported the same deterministic payload digest:

```text
a45ce32596d81f615790d57c31c4f2157281f2292f8bfb6f6b88911fc757822e
```

A byte comparison confirmed that the two JSON files were identical, and Python compilation completed successfully.

This verifies deterministic replay for the tested environment and seed.

---

## Slide 11 — How to Reproduce the Result

To reproduce the sample report from the repository root, run:

```bash
python3 astro_membrane_sim.py \\
  --seed 7 \\
  --report sample_astro_report.json
```

To use a different deterministic scenario, provide another integer seed and a different output path:

```bash
python3 astro_membrane_sim.py --seed 42 --report report_seed_42.json
```

A changed seed is expected to change the generated bulk and velocity vectors, and therefore the resulting digest. Repeating the same seed and configuration should reproduce the same artifact.

---

## Slide 12 — Scope and Limitations

The prototype demonstrates software structure and reproducibility, not aerospace readiness.

Its numerical models are intentionally simple. They do not include orbital dynamics, relativistic corrections, sensor calibration procedures, fault-tolerant control, hardware interfaces, uncertainty propagation, or flight certification requirements.

Floating-point results are deterministic for the tested Python environment and configuration. If portability across different runtimes or hardware becomes a requirement, the project should add a defined numerical compatibility policy and targeted cross-platform tests.

The synthetic labels and explicit limitations are part of the design. They prevent the prototype from being mistaken for validated spacecraft software.

---

## Closing

To summarize, the astro membrane simulation is organized as four independent analytical lanes connected by a small deterministic driver.

The determinism fix removes the runtime timestamp from the report, seeds all pseudo-random generation, serializes JSON canonically, and records a SHA-256 digest over the deterministic content.

That combination provides a transparent and repeatable research artifact: the same inputs lead to the same report, while the architecture remains modular enough for future testing or replacement of individual simulation components.

Thank you.


---

## Appendix — Orbital Phase-Field Extension

The repository now includes `orbital_phase_field_engine.py`, a second synthetic research engine built around a scalar phase field.

Its energy model combines three terms: a gradient contribution, a double-well potential `V(phi) = phi^2(1-phi)^2`, and a crystallization penalty weighted by the damping gain. The engine reports each term separately as well as their total, making the calculation auditable rather than presenting only a final score.

The implementation is fail-closed. Phase order must remain within `[0, 1]`; gradient and crystallization terms must be non-negative; and every numeric input must be finite. Invalid values raise an exception rather than being silently clamped or converted into a plausible-looking result.

One scientific logic defect in the original attachment was corrected. The condition `V(phi) > 0.15` could never be true because the maximum of the double-well potential on `[0, 1]` is `1/16`, or `0.0625`. The updated engine uses an explicit, configurable phase-lock threshold of `0.80`, while retaining the crystallization-index threshold as a separate gate.

The trajectory generator uses `random.Random(seed)` rather than the process-wide random generator. This preserves deterministic replay and prevents the simulation from changing random sequences in unrelated code.

The new regression suite checks exact energy terms, invalid-input rejection, reachable phase locking, same-seed equality, different-seed divergence, zero-step behavior, and preservation of global random state.

This extension strengthens the repository's scientific posture by making assumptions explicit, identifying unreachable logic, and testing both numerical behavior and reproducibility.


---

## Appendix — Unified Master Engine

The repository now includes `sparkainlp_master_engine.py`, which composes the four validated lanes into a single audit-oriented testbench.

The master flow begins with a seeded synthetic bulk vector and velocity vector. The membrane mapper produces boundary summaries. The phase-field engine evaluates free energy and crystallization status. The synchronization predictor estimates delayed telemetry. Finally, the calibrator checks readings against positivity and invariant-drift rules.

The composition is deterministic without pretending to be physical flight software. The master engine omits runtime timestamps, uses a private pseudo-random generator, validates all finite numeric inputs, and hashes canonical JSON.

The original master attachment contained the same unreachable condition identified in the phase-field prototype: `V(phi) > 0.15` cannot occur on the admissible interval because the double-well maximum is `0.0625`. The integrated engine uses the corrected explicit phase-lock threshold from the hardened phase-field implementation.

The master report records the four lane outputs under `simulation_results`. Its regression tests verify reproducibility, seed sensitivity, non-finite-value rejection, telemetry shape validation, negative-tick rejection, and the presence of all four lanes.


---

## Appendix — Advanced Stochastic and Provenance Engine

The latest extension is `sparkainlp_advanced_science_engine.py`.

It adds a bounded Euler-Maruyama-style phase experiment. The phase update uses the derivative of the double-well potential, a gradient contribution, an anti-crystallization damping force, and an explicitly supplied thermal-noise sample. The runner draws noise from a private seeded RNG, while the update method itself remains reproducible for explicit inputs.

The extension also computes synthetic boundary action metrics. Bulk values are grouped into cells, summarized by RMS energy and peak amplitude, and transformed into an action-density score. These are software-defined metrics for comparative simulation only; they are not a derivation of a physical holographic-complexity observable.

Every advanced report is timestamp-free. A canonical JSON manifest is hashed before the provenance field is added, avoiding self-reference. Repeated executions with the same seed, iteration count, and time step therefore produce identical reports and identical provenance digests.

The implementation rejects non-finite values, invalid phase bounds, negative gradient or crystallization terms, non-positive integration steps, and negative bulk values in the logarithmic action metric. These guardrails make invalid states visible instead of silently converting them into plausible output.

The source attachment's `V(phi) > 0.15` lock test was again corrected because the double-well potential cannot exceed `0.0625` on `[0, 1]`. The advanced engine uses the same reachable explicit phase threshold as the validated phase-field engine.


---

## Appendix — Next-Discovery Diagnostics

The next extension is `sparkainlp_next_discovery_engine.py`.

Its first lane is an RG-like coupling-flow map. It evolves a non-negative coupling using an explicit scaling dimension, determination factor, and integration step, then reports drift from a configured target. This is a parameterized numerical diagnostic, not an exact renormalization-group derivation.

Its second lane computes an entropy-to-capacity metric from non-negative subregion densities. Empty input is handled explicitly, preventing division by zero. The metric is useful for comparing synthetic configurations, but it is not a literal Ryu–Takayanagi minimal-surface calculation.

Its third lane applies a scalar gauge-correction surrogate and reports whether the corrected phase lies within an explicit lock-risk threshold. The scalar input is deliberately labeled as a surrogate; it is not a non-Abelian gauge-field tensor or a proof of topological defect neutralization.

Like the other engines, the next-discovery report excludes runtime timestamps, uses a private seeded RNG, validates finite numeric domains, and binds the report payload to a canonical SHA-256 provenance manifest. Regression tests cover same-seed replay, different-seed divergence, empty entropy capacity, invalid inputs, gauge lock risk, and global RNG isolation.


---

## Appendix — Spinning Cascade Diagnostics

The new `spinning_cascade_engine.py` models a ring of synthetic nodes under a scalar rotational-energy surrogate.

Each node receives a non-negative raw energy and a radial coordinate. The engine adds `1/2 omega^2 r^2`, described correctly as rotational potential energy per unit mass, and compares the effective energy with a cascade threshold. The ring report includes every node, active-cascade count, active fraction, and a contained-versus-avalanche summary.

The ring generator uses a private seeded random stream. Node evaluation is deterministic for explicit inputs, and the full timestamp-free report is bound to a canonical SHA-256 provenance manifest.

The model does not solve rotating-frame equations, include Coriolis vectors, simulate vortices, or demonstrate physical crystallization control. Those claims would require a defined continuum model, coordinate conventions, dimensional analysis, numerical convergence studies, and empirical validation.
