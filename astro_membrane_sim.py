#!/usr/bin/env python3
"""
astro_membrane_sim.py
--------------------------------------------------------------------------------
Research Prototype: Four Astro-Holographic Simulation & Calibration Modules
Copyright (c) 2026 Jean-François Brisson / Spark AI NLP
License: AGPL-3.0-only (see LICENSE)

HONESTY & SIMULATION LABELS:
- SYNTHETIC DEMO ONLY: All data structures, telemetry streams, and orbital
  parameters are simulated classical models. No hardware experiment performed.
- NO ASTROPHYSICAL CLAIM: This software does not control spacecraft, connect to
  orbital sensors, or replace flight-certified navigation software.
- SEPARATION OF LANES: Holographic boundary compression, anti-crystallization,
  relativistic synchronization, and self-knowing calibration operate as
  independent simulation lanes with no hidden shared state.
- DETERMINISM: Runtime timestamps are intentionally excluded from the report so
  identical seeds produce byte-for-byte identical JSON and SHA-256 output.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math
import random

VERSION = "0.1.1"


class HolographicBoundaryMapper:
    """Lane 1: AdS/CFT-style volumetric compression to boundary state vector."""

    def __init__(self, cell_width=32, total_cells=4):
        self.cell_width = cell_width
        self.total_channels = cell_width * total_cells

    def compress_bulk(self, bulk_volume_matrix):
        """Compress a 3D/volumetric sensor matrix into a 2D boundary vector."""
        boundary_vector = []
        for cell_idx in range(0, len(bulk_volume_matrix), self.cell_width):
            cell = bulk_volume_matrix[cell_idx:cell_idx + self.cell_width]
            if not cell:
                continue
            # Boundary projection: RMS energy and max anomaly per cell.
            rms = math.sqrt(sum(x**2 for x in cell) / len(cell))
            peak = max(cell)
            boundary_vector.append({
                "cell_id": cell_idx // self.cell_width,
                "rms": rms,
                "peak": peak,
            })
        return boundary_vector


class AntiCrystallizationGuard:
    """Lane 2: Combat premature structural locking via phase damping."""

    def __init__(self, tolerance_tau=0.25):
        self.tau = tolerance_tau

    def evaluate_phase(self, phase_order_parameter, crystallization_index):
        """Return residual discrepancy and whether crystallization is imminent."""
        residual = abs(phase_order_parameter - 1.0)
        is_locked = (crystallization_index > self.tau) or (residual > self.tau)
        return {
            "phase_order": phase_order_parameter,
            "crystallization_index": crystallization_index,
            "residual": residual,
            "locked": is_locked,
            "action": "DAMPING_APPLIED" if is_locked else "FLUID_ADAPTIVE",
        }


class RelativisticSyncEngine:
    """Lane 3: Mitigate light-lag between operators and autonomous agents."""

    def __init__(self, light_lag_seconds=1.2):
        self.lag = light_lag_seconds

    def predict_state(self, local_telemetry, velocity_vector, elapsed_ticks):
        """Simulate predictive states during interplanetary communication lag."""
        simulated_state = []
        for i, val in enumerate(local_telemetry):
            drift = velocity_vector[i] * (elapsed_ticks + self.lag)
            simulated_state.append(val + drift)
        return simulated_state


class SelfKnowingCalibrator:
    """Lane 4: Internal navigation verification without external GPS."""

    def __init__(self, invariant_target=1.0):
        self.target = invariant_target

    def verify_calibration(self, sensor_readings, absolute_uncertainty=0.01):
        """Evaluate internal telemetry against conservation invariants."""
        valid_samples = []
        for reading in sensor_readings:
            lower_bound = reading - absolute_uncertainty
            is_valid = (reading > 0.0) and (lower_bound > 0.0)
            valid_samples.append({
                "reading": reading,
                "lower_bound": lower_bound,
                "admissible": is_valid,
            })

        all_admissible = all(sample["admissible"] for sample in valid_samples)
        mean_val = (
            sum(sample["reading"] for sample in valid_samples) / len(valid_samples)
            if valid_samples else 0.0
        )
        drift_delta = abs(mean_val - self.target)

        return {
            "all_admissible": all_admissible,
            "mean_telemetry": mean_val,
            "invariant_drift": drift_delta,
            "calibration_status": (
                "LOCKED" if (all_admissible and drift_delta < 0.05)
                else "DRIFT_REJECTED"
            ),
        }


def run_simulation(seed=42):
    random.seed(seed)

    # Initialize components.
    membrane = HolographicBoundaryMapper(cell_width=32, total_cells=2)
    anti_crys = AntiCrystallizationGuard(tolerance_tau=0.25)
    rel_sync = RelativisticSyncEngine(light_lag_seconds=1.5)
    calibrator = SelfKnowingCalibrator(invariant_target=1.0)

    # Synthetic input vectors.
    bulk_data = [random.uniform(0.1, 0.9) for _ in range(64)]
    velocities = [random.uniform(-0.02, 0.02) for _ in range(64)]
    sensor_data = [1.002, 0.998, 1.001, 1.004]

    # Execute simulation lanes.
    boundary_res = membrane.compress_bulk(bulk_data)
    crys_res = anti_crys.evaluate_phase(
        phase_order_parameter=0.82,
        crystallization_index=0.15,
    )
    sync_res = rel_sync.predict_state(
        bulk_data[:10],
        velocities[:10],
        elapsed_ticks=3,
    )
    cal_res = calibrator.verify_calibration(sensor_data)

    # Deliberately omit a runtime timestamp: it would make the JSON and its
    # digest differ on every execution, even when the seed is unchanged.
    return {
        "metadata": {
            "generator": "astro_membrane_sim.py",
            "version": VERSION,
            "seed": seed,
            "data_kind": "synthetic_illustrative",
            "determinism": "runtime timestamp excluded",
        },
        "results": {
            "holographic_boundary": boundary_res,
            "anti_crystallization": crys_res,
            "relativistic_sync_sample": sync_res[:3],
            "self_knowing_calibration": cal_res,
        },
    }


def canonical_json_bytes(payload):
    """Serialize a payload canonically for stable hashing across reruns."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def deterministic_sha256(report):
    """Hash the deterministic report content, excluding the hash field itself."""
    return hashlib.sha256(canonical_json_bytes(report)).hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Astro-Holographic Simulation Prototype"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for determinism",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="astro_challenge_report.json",
        help="Output JSON path",
    )
    args = parser.parse_args()

    report = run_simulation(seed=args.seed)
    report_hash = deterministic_sha256(report)
    report["metadata"]["deterministic_sha256"] = report_hash

    with open(args.report, "w", encoding="utf-8") as output_file:
        json.dump(report, output_file, indent=2, ensure_ascii=False)
        output_file.write("\n")

    print(f"[SUCCESS] Simulation completed successfully using seed {args.seed}.")
    print(f"Report written to: {args.report}")
    print(f"Deterministic SHA-256: {report_hash}")
    print(json.dumps(report["results"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
