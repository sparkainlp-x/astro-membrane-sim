#!/usr/bin/env python3
"""
orbital_phase_field_engine.py
--------------------------------------------------------------------------------
Research Engine: Orbital Phase-Field & Anti-Crystallization Damping Protocol
Copyright (c) 2026 Jean-François Brisson / Spark AI NLP
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC NUMERICAL MODEL: Implements theoretical free-energy functionals
  and phase-field evolution rules for research simulation.
- NO HARDWARE/FLIGHT CONTROL CLAIM: This script executes software testbenches
  only. It does not interface directly with physical aerospace hardware or
  active manufacturing machinery.
- ZERO HIDDEN STATE: Functional evaluations are pure with respect to their
  explicit arguments and engine configuration. Simulation RNG state is local.
- DETERMINISM: Runtime timestamps and external state are excluded from reports.
  Identical seeds and parameters produce identical JSON and SHA-256 values.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math
import random
from numbers import Real

VERSION = "0.2.1"


def _require_finite_real(name, value):
    """Return a finite real value or fail closed with a useful error."""
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number; got {value!r}.")
    return float(value)


class OrbitalPhaseFieldEngine:
    """Evaluate phase-field free energy and anti-crystallization risk."""

    def __init__(
        self,
        tolerance_tau=0.20,
        damping_gain=0.85,
        phase_lock_threshold=0.80,
    ):
        self.tau = _require_finite_real("tolerance_tau", tolerance_tau)
        self.gamma = _require_finite_real("damping_gain", damping_gain)
        self.phase_lock_threshold = _require_finite_real(
            "phase_lock_threshold", phase_lock_threshold
        )
        if self.tau < 0.0:
            raise ValueError("tolerance_tau must be non-negative.")
        if self.gamma < 0.0:
            raise ValueError("damping_gain must be non-negative.")
        if not 0.0 <= self.phase_lock_threshold <= 1.0:
            raise ValueError("phase_lock_threshold must be within [0, 1].")

    def compute_free_energy(self, phi, gradient_norm_sq, crys_index):
        """
        Compute the scalar free-energy density:

            G(phi) = 1/2 |grad phi|^2 + V(phi) + gamma * crys_index^2
            V(phi) = phi^2 * (1 - phi)^2

        ``phi`` is constrained to [0, 1]. Gradient and crystallization terms
        must be finite and non-negative. Invalid inputs fail closed.
        """
        phi = _require_finite_real("phi", phi)
        gradient_norm_sq = _require_finite_real(
            "gradient_norm_sq", gradient_norm_sq
        )
        crys_index = _require_finite_real("crys_index", crys_index)

        if not 0.0 <= phi <= 1.0:
            raise ValueError(
                f"Phase order parameter phi={phi} out of admissible bound [0, 1]."
            )
        if gradient_norm_sq < 0.0 or crys_index < 0.0:
            raise ValueError(
                "Crystallization index and gradient norm squared must be non-negative."
            )

        double_well = (phi ** 2) * ((1.0 - phi) ** 2)
        penalty = self.gamma * (crys_index ** 2)
        total_energy = 0.5 * gradient_norm_sq + double_well + penalty

        # The original attachment used double_well > 0.15. That branch is
        # unreachable because max(phi^2 * (1-phi)^2) = 1/16. An explicit
        # phase threshold makes the intended high-order locking test reachable
        # and auditable while retaining crystallization-index gating.
        is_locked = (
            crys_index > self.tau
            or phi >= self.phase_lock_threshold
        )
        action = "APPLY_FEEDBACK_DAMPING" if is_locked else "MAINTAIN_FLUID_FLOW"

        return {
            "phi": phi,
            "gradient_norm_sq": gradient_norm_sq,
            "crystallization_index": crys_index,
            "double_well_potential": double_well,
            "crystallization_penalty": penalty,
            "total_free_energy": total_energy,
            "crystallization_locked": is_locked,
            "engine_action": action,
        }


def run_simulation_suite(seed=42, steps=5, engine=None):
    """Run a deterministic synthetic trajectory using a private RNG stream."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer.")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError("steps must be a non-negative integer.")

    local_rng = random.Random(seed)
    engine = engine or OrbitalPhaseFieldEngine()
    trajectory_log = []
    phi_val = 0.1

    # Synthetic temporal evolution under modeled thermal/microgravity shifts.
    for step in range(steps):
        phi_val = min(1.0, max(0.0, phi_val + local_rng.uniform(0.05, 0.25)))
        grad_sq = local_rng.uniform(0.01, 0.1)
        crys_idx = local_rng.uniform(0.05, 0.40)

        result = engine.compute_free_energy(phi_val, grad_sq, crys_idx)
        result["step"] = step
        trajectory_log.append(result)

    return {
        "metadata": {
            "engine": "orbital_phase_field_engine.py",
            "version": VERSION,
            "seed": seed,
            "steps": steps,
            "epistemic_status": "synthetic_research_model",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "trajectory": trajectory_log,
    }


def canonical_json_bytes(payload):
    """Serialize JSON canonically for stable hashing."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def deterministic_sha256(report):
    """Hash a report before its digest field is added."""
    return hashlib.sha256(canonical_json_bytes(report)).hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Orbital Phase-Field & Anti-Crystallization Engine"
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed")
    parser.add_argument(
        "--steps", type=int, default=5, help="Non-negative trajectory length"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="phase_field_audit_report.json",
        help="Output JSON audit file",
    )
    args = parser.parse_args()

    try:
        report = run_simulation_suite(seed=args.seed, steps=args.steps)
        report_hash = deterministic_sha256(report)
        report["metadata"]["deterministic_sha256"] = report_hash

        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")

        print(f"[SUCCESS] Phase-field audit completed using seed {args.seed}.")
        print(f"Report saved to: {args.output}")
        print(f"Deterministic SHA-256: {report_hash}")
        if report["trajectory"]:
            print(json.dumps(report["trajectory"][-1], indent=2))
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] Simulation aborted: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
