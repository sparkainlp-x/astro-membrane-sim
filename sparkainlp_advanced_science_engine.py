#!/usr/bin/env python3
"""
sparkainlp_advanced_science_engine.py
--------------------------------------------------------------------------------
Advanced Research Engine: Stochastic Phase-Field & Holographic Complexity Protocol
Copyright (c) 2026 Jean-François Brisson / Spark AI NLP
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC RESEARCH TESTBENCH: Implements a bounded Euler-Maruyama-style
  phase-field experiment, boundary action metrics, and provenance manifests.
- NO HARDWARE/FLIGHT CONTROL CLAIM: This is not flight-certified software and
  does not interface with spacecraft, sensors, or manufacturing machinery.
- ZERO HIDDEN STATE: The phase update is pure for explicit inputs, including
  the sampled thermal-noise value. The runner owns a private seeded RNG.
- DETERMINISM: Runtime timestamps and external state are excluded from reports.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math
import random
from numbers import Real

VERSION = "2.0.1"


def _finite_real(name, value):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number; got {value!r}.")
    return float(value)


class StochasticPhaseFieldSimulator:
    """Bounded phase-field update with an explicit thermal-noise sample."""

    def __init__(self, tolerance_tau=0.20, damping_gain=0.85, mobility=1.0):
        self.tau = _finite_real("tolerance_tau", tolerance_tau)
        self.gamma = _finite_real("damping_gain", damping_gain)
        self.mobility = _finite_real("mobility", mobility)
        if self.tau < 0.0 or self.gamma < 0.0 or self.mobility < 0.0:
            raise ValueError("tolerance_tau, damping_gain, and mobility must be non-negative.")

    def step_evolution(
        self,
        phi,
        grad_sq,
        crys_index,
        noise=0.0,
        dt=0.01,
    ):
        """Perform one bounded Euler-Maruyama-style synthetic phase update.

        The caller supplies ``noise`` explicitly. This keeps the mathematical
        update reproducible and testable without hidden RNG state.
        """
        phi = _finite_real("phi", phi)
        grad_sq = _finite_real("grad_sq", grad_sq)
        crys_index = _finite_real("crys_index", crys_index)
        noise = _finite_real("noise", noise)
        dt = _finite_real("dt", dt)

        if not 0.0 <= phi <= 1.0:
            raise ValueError(f"Phase parameter phi={phi} out of admissible bound [0, 1].")
        if grad_sq < 0.0 or crys_index < 0.0:
            raise ValueError("grad_sq and crys_index must be non-negative.")
        if dt <= 0.0:
            raise ValueError("dt must be positive.")

        dv_dphi = 2.0 * phi * (1.0 - phi) * (1.0 - 2.0 * phi)
        damping_force = self.gamma * crys_index
        drift = -self.mobility * (dv_dphi - 0.5 * grad_sq + damping_force)
        d_phi_dt = drift + noise
        new_phi = max(0.0, min(1.0, phi + d_phi_dt * dt))
        double_well = new_phi ** 2 * (1.0 - new_phi) ** 2

        # As in the hardened phase-field engine, use a reachable explicit
        # crystallization threshold rather than the impossible V(phi) > 0.15.
        is_locked = crys_index > self.tau or new_phi >= 0.80
        return {
            "phi_previous": phi,
            "phi_updated": new_phi,
            "double_well_potential": double_well,
            "crystallization_index": crys_index,
            "thermal_noise": noise,
            "d_phi_dt": d_phi_dt,
            "crystallization_locked": is_locked,
            "action": "APPLY_FEEDBACK_DAMPING" if is_locked else "MAINTAIN_FLUID_FLOW",
        }


class HolographicComplexityAnalyzer:
    """Compute synthetic boundary action and complexity summary metrics."""

    def __init__(self, cell_width=32):
        if isinstance(cell_width, bool) or not isinstance(cell_width, int) or cell_width <= 0:
            raise ValueError("cell_width must be a positive integer.")
        self.cell_width = cell_width

    def compute_boundary_complexity(self, bulk_matrix):
        values = [_finite_real("bulk value", value) for value in bulk_matrix]
        if any(value < 0.0 for value in values):
            raise ValueError("bulk values must be non-negative for log-scaled action metrics.")

        boundary_nodes = []
        total_action = 0.0
        for idx in range(0, len(values), self.cell_width):
            cell = values[idx:idx + self.cell_width]
            if not cell:
                continue
            rms = math.sqrt(sum(value ** 2 for value in cell) / len(cell))
            peak = max(cell)
            cell_action = rms * math.log(max(peak, 1e-6))
            total_action += abs(cell_action)
            boundary_nodes.append({
                "cell_id": idx // self.cell_width,
                "rms_energy": rms,
                "peak_amplitude": peak,
                "action_density": cell_action,
            })

        return {
            "boundary_nodes": boundary_nodes,
            "total_bulk_action": total_action,
            "holographic_complexity_score": total_action / math.pi,
        }


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


def execute_advanced_simulation(seed=42, iterations=3, dt=0.01):
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer.")
    if isinstance(iterations, bool) or not isinstance(iterations, int) or iterations < 0:
        raise ValueError("iterations must be a non-negative integer.")
    dt = _finite_real("dt", dt)
    if dt <= 0.0:
        raise ValueError("dt must be positive.")

    local_rng = random.Random(seed)
    complexity_analyzer = HolographicComplexityAnalyzer(cell_width=16)
    phase_simulator = StochasticPhaseFieldSimulator()
    bulk_data = [local_rng.uniform(0.1, 0.9) for _ in range(48)]

    phase_trajectory = []
    current_phi = 0.25
    for iteration in range(iterations):
        crys_index = local_rng.uniform(0.05, 0.35)
        grad_sq = local_rng.uniform(0.01, 0.08)
        thermal_noise = local_rng.gauss(0.0, 0.02)
        result = phase_simulator.step_evolution(
            current_phi,
            grad_sq,
            crys_index,
            noise=thermal_noise,
            dt=dt,
        )
        result["iteration"] = iteration
        phase_trajectory.append(result)
        current_phi = result["phi_updated"]

    payload = {
        "metadata": {
            "engine": "sparkainlp_advanced_science_engine.py",
            "version": VERSION,
            "seed": seed,
            "iterations": iterations,
            "dt": dt,
            "epistemic_status": "synthetic_research_model",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "simulation_results": {
            "holographic_complexity_analysis": complexity_analyzer.compute_boundary_complexity(
                bulk_data
            ),
            "stochastic_phase_trajectory": phase_trajectory,
        },
    }
    payload["provenance_sha256"] = CryptographicProvenanceLedger.generate_manifest(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Spark AI NLP Advanced Science Research Engine"
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed")
    parser.add_argument("--iterations", type=int, default=3, help="Non-negative SDE steps")
    parser.add_argument("--dt", type=float, default=0.01, help="Positive integration step")
    parser.add_argument(
        "--output",
        type=str,
        default="advanced_science_audit.json",
        help="Output audit report path",
    )
    args = parser.parse_args()

    try:
        report = execute_advanced_simulation(
            seed=args.seed,
            iterations=args.iterations,
            dt=args.dt,
        )
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] Advanced simulation completed using seed {args.seed}.")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] Simulation aborted: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
