#!/usr/bin/env python3
"""
spinning_cascade_engine.py
--------------------------------------------------------------------------------
Research Engine: Spin-Mediated Cascade Dynamics & Rotational Phase Control
Copyright (c) 2026 Jean-François Brisson / Spark AI NLP
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC RESEARCH TESTBENCH: Implements a scalar rotational-energy
  surrogate, thresholded cascade events, and ring-level summary metrics.
- NO HARDWARE/FLIGHT CONTROL CLAIM: This is not a physical rotating-frame
  solver, manufacturing controller, or flight-certified system.
- ZERO HIDDEN STATE: Node evaluation is pure for explicit inputs; the ring
  runner uses a private seeded RNG and timestamp-free canonical reports.
- DETERMINISM: Identical seeds and parameters produce identical JSON and hashes.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math
import random
from numbers import Real

VERSION = "1.1.0"


def _finite_real(name, value):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number; got {value!r}.")
    return float(value)


class SpinningCascadeSimulator:
    """Evaluate thresholded cascade risk under a scalar rotation surrogate."""

    def __init__(self, angular_velocity=1.5, cascade_threshold=0.75):
        self.omega = _finite_real("angular_velocity", angular_velocity)
        self.threshold = _finite_real("cascade_threshold", cascade_threshold)
        if self.omega < 0.0:
            raise ValueError("angular_velocity must be non-negative.")
        if self.threshold < 0.0:
            raise ValueError("cascade_threshold must be non-negative.")

    def evaluate_node_cascade(self, node_energy, rotational_radius):
        node_energy = _finite_real("node_energy", node_energy)
        rotational_radius = _finite_real("rotational_radius", rotational_radius)
        if node_energy < 0.0 or rotational_radius < 0.0:
            raise ValueError(
                "node_energy and rotational_radius must be non-negative."
            )

        # This is centrifugal potential energy per unit mass, not force:
        # E_rot = 1/2 * omega^2 * r^2.
        rotational_potential_energy = (
            0.5 * self.omega ** 2 * rotational_radius ** 2
        )
        effective_energy = node_energy + rotational_potential_energy
        is_cascading = effective_energy >= self.threshold
        cascade_intensity = (
            effective_energy - self.threshold if is_cascading else 0.0
        )

        return {
            "raw_energy": node_energy,
            "rotational_radius": rotational_radius,
            "rotational_potential_energy": rotational_potential_energy,
            "effective_energy": effective_energy,
            "cascade_triggered": is_cascading,
            "cascade_intensity": cascade_intensity,
            "status": "AVALANCHE_ACTIVE" if is_cascading else "VORTEX_STABLE",
        }


class SpinningMembraneArray:
    """Generate a deterministic ring of synthetic rotating nodes."""

    def __init__(self, node_count=32, base_radius=0.1, radius_step=0.05):
        if isinstance(node_count, bool) or not isinstance(node_count, int) or node_count < 0:
            raise ValueError("node_count must be a non-negative integer.")
        self.node_count = node_count
        self.base_radius = _finite_real("base_radius", base_radius)
        self.radius_step = _finite_real("radius_step", radius_step)
        if self.base_radius < 0.0 or self.radius_step < 0.0:
            raise ValueError("base_radius and radius_step must be non-negative.")

    def simulate_rotation_ring(self, simulator, rng):
        if not isinstance(rng, random.Random):
            raise TypeError("rng must be a private random.Random instance.")
        ring_results = []
        for node_id in range(self.node_count):
            radius = self.base_radius + node_id * self.radius_step
            energy = rng.uniform(0.3, 0.9)
            node_result = simulator.evaluate_node_cascade(energy, radius)
            node_result["node_id"] = node_id
            ring_results.append(node_result)
        return ring_results


class CryptographicProvenanceLedger:
    """Create canonical SHA-256 manifests for deterministic audit artifacts."""

    @staticmethod
    def canonical_bytes(payload):
        return json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")

    @classmethod
    def generate_manifest(cls, payload):
        return hashlib.sha256(cls.canonical_bytes(payload)).hexdigest()


def execute_spinning_cascade_simulation(seed=42):
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer.")

    local_rng = random.Random(seed)
    simulator = SpinningCascadeSimulator(
        angular_velocity=2.0,
        cascade_threshold=0.80,
    )
    array = SpinningMembraneArray(node_count=16)
    ring_telemetry = array.simulate_rotation_ring(simulator, local_rng)
    active_cascades = sum(
        1 for node in ring_telemetry if node["cascade_triggered"]
    )
    active_fraction = active_cascades / len(ring_telemetry) if ring_telemetry else 0.0

    payload = {
        "metadata": {
            "engine": "spinning_cascade_engine.py",
            "version": VERSION,
            "seed": seed,
            "epistemic_status": "synthetic_research_model",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "simulation_results": {
            "total_nodes": len(ring_telemetry),
            "active_cascade_count": active_cascades,
            "active_cascade_fraction": active_fraction,
            "system_stability": (
                "CONTAINED_VORTEX" if active_fraction < 0.5
                else "RECURSIVE_AVALANCHE"
            ),
            "node_telemetry": ring_telemetry,
        },
    }
    payload["provenance_sha256"] = CryptographicProvenanceLedger.generate_manifest(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Spin-Mediated Cascade Dynamics Simulator"
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed")
    parser.add_argument(
        "--output",
        type=str,
        default="spinning_cascade_audit.json",
        help="Output audit report path",
    )
    args = parser.parse_args()

    try:
        report = execute_spinning_cascade_simulation(seed=args.seed)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] Spinning cascade simulation completed using seed {args.seed}.")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
        print(json.dumps(report["simulation_results"], indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] Simulation failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
