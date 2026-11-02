#!/usr/bin/env python3
"""
energy_phase_engine.py
--------------------------------------------------------------------------------
Breakout Track 2: Materials & Energy Phase-Field Dynamics Diagnostic
Copyright (c) 2026 Hicham JF Brisson / Spark AI NLP (sparkainlp-x)
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC RESEARCH TESTBENCH: Implements a bounded Euler-Maruyama-style
  phase update and an explicitly labeled rotational-damping surrogate.
- NO INDUSTRIAL MANUFACTURING CLAIM: Not connected to foundry equipment,
  orbital manufacturing hardware, or physical casting lines.
- ZERO HIDDEN STATE: Noise is explicit to the phase step and sampled from a
  private seeded RNG by the runner.
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


class EnergyPhaseFieldSimulator:
    """Bounded stochastic phase evolution with explicit noise and damping terms."""

    def __init__(self, tolerance_tau=0.20, damping_gain=0.85, mobility=1.0):
        self.tau = _finite_real("tolerance_tau", tolerance_tau)
        self.gamma = _finite_real("damping_gain", damping_gain)
        self.mobility = _finite_real("mobility", mobility)
        if self.tau < 0.0 or self.gamma < 0.0 or self.mobility < 0.0:
            raise ValueError("tolerance_tau, damping_gain, and mobility must be non-negative.")

    def step_phase_evolution(
        self,
        phi,
        grad_sq,
        crys_index,
        noise=0.0,
        dt=0.01,
        rotational_damping=0.0,
    ):
        phi = _finite_real("phi", phi)
        grad_sq = _finite_real("grad_sq", grad_sq)
        crys_index = _finite_real("crys_index", crys_index)
        noise = _finite_real("noise", noise)
        dt = _finite_real("dt", dt)
        rotational_damping = _finite_real(
            "rotational_damping", rotational_damping
        )
        if not 0.0 <= phi <= 1.0:
            raise ValueError(f"Phase parameter phi={phi} out of admissible bound [0, 1].")
        if grad_sq < 0.0 or crys_index < 0.0 or rotational_damping < 0.0:
            raise ValueError(
                "grad_sq, crys_index, and rotational_damping must be non-negative."
            )
        if dt <= 0.0:
            raise ValueError("dt must be positive.")

        dv_dphi = 2.0 * phi * (1.0 - phi) * (1.0 - 2.0 * phi)
        phase_damping = self.gamma * crys_index
        total_damping = phase_damping + rotational_damping
        drift = -self.mobility * (dv_dphi - 0.5 * grad_sq + total_damping)
        d_phi_dt = drift + noise
        new_phi = max(0.0, min(1.0, phi + d_phi_dt * dt))
        double_well = new_phi ** 2 * (1.0 - new_phi) ** 2
        is_locked = crys_index > self.tau or new_phi >= 0.80
        return {
            "phi_previous": phi,
            "phi_updated": new_phi,
            "double_well_potential": double_well,
            "crystallization_index": crys_index,
            "phase_damping": phase_damping,
            "rotational_damping": rotational_damping,
            "thermal_noise": noise,
            "d_phi_dt": d_phi_dt,
            "crystallization_locked": is_locked,
            "phase_action": (
                "APPLY_FEEDBACK_DAMPING" if is_locked
                else "MAINTAIN_FLUID_FLOW"
            ),
            "epistemic_label": "BOUNDED_SYNTHETIC_PHASE_FIELD",
        }


class CentrifugalDampingSurrogate:
    """Compute a transparent scalar rotational-potential damping surrogate."""

    def __init__(self, angular_velocity=1.0, radius=0.5, damping_gain=0.05):
        self.omega = _finite_real("angular_velocity", angular_velocity)
        self.radius = _finite_real("radius", radius)
        self.gain = _finite_real("damping_gain", damping_gain)
        if self.omega < 0.0 or self.radius < 0.0 or self.gain < 0.0:
            raise ValueError("rotational parameters must be non-negative.")

    def compute(self):
        potential_energy = 0.5 * self.omega ** 2 * self.radius ** 2
        return {
            "angular_velocity": self.omega,
            "radius": self.radius,
            "rotational_potential_energy": potential_energy,
            "damping_surrogate": self.gain * potential_energy,
            "epistemic_label": "SCALAR_ROTATIONAL_DAMPING_SURROGATE",
        }


class ElevenDimensionalObserver:
    """Evaluate nine telemetry dimensions plus two observer-proxy axes."""

    spatial_dims = 9
    observer_dims = 2

    def calibrate_axes(self, raw_telemetry, human_empathy_intent_score):
        telemetry = [_finite_real("raw telemetry", value) for value in raw_telemetry]
        if len(telemetry) != self.spatial_dims:
            raise ValueError("raw_telemetry must contain exactly 9 values.")
        empathy = _finite_real(
            "human_empathy_intent_score", human_empathy_intent_score
        )
        if not 0.0 <= empathy <= 1.0:
            raise ValueError("Empathy proxy must be normalized within [0, 1].")
        d10 = sum(math.sin(value) for value in telemetry) / self.spatial_dims
        magnitude = math.sqrt(sum(value ** 2 for value in telemetry) + d10 ** 2 + empathy ** 2)
        return {
            "spatial_dimensions": self.spatial_dims,
            "observer_dimensions": self.observer_dims,
            "d10_self_knowing_factor": d10,
            "d11_empathetic_alignment_proxy": empathy,
            "eleven_d_magnitude": magnitude,
            "social_proxy_status": (
                "ALIGNMENT_PROXY_PASS" if empathy >= 0.70
                else "ALIGNMENT_PROXY_RECALIBRATION_REQUIRED"
            ),
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


def _success_criteria(results):
    phase = results["phase_field_dynamics"]
    observer = results["eleven_dimensional_calibration"]
    criteria = {
        "phase_state_bounded": 0.0 <= phase["phi_updated"] <= 1.0,
        "phase_outputs_finite": all(
            math.isfinite(phase[key])
            for key in ("phi_updated", "double_well_potential", "d_phi_dt")
        ),
        "rotational_damping_finite": math.isfinite(
            phase["rotational_damping"]
        ),
        "nine_plus_two_dimensions_present": (
            observer["spatial_dimensions"] == 9
            and observer["observer_dimensions"] == 2
        ),
        "empathy_alignment_proxy_pass": (
            observer["d11_empathetic_alignment_proxy"] >= 0.70
        ),
    }
    return {
        "criteria": criteria,
        "overall_success": all(criteria.values()),
        "interpretation": (
            "All synthetic phase-field gates passed"
            if all(criteria.values())
            else "One or more synthetic phase-field gates failed"
        ),
    }


def execute_energy_simulation(seed=42):
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer.")

    local_rng = random.Random(seed)
    phase_simulator = EnergyPhaseFieldSimulator()
    rotational_model = CentrifugalDampingSurrogate()
    observer = ElevenDimensionalObserver()
    telemetry_9d = [local_rng.uniform(0.2, 0.9) for _ in range(9)]
    rotational_result = rotational_model.compute()
    phase_result = phase_simulator.step_phase_evolution(
        phi=0.35,
        grad_sq=0.04,
        crys_index=0.12,
        noise=local_rng.gauss(0.0, 0.02),
        rotational_damping=rotational_result["damping_surrogate"],
    )
    results = {
        "phase_field_dynamics": phase_result,
        "rotational_damping_surrogate": rotational_result,
        "eleven_dimensional_calibration": observer.calibrate_axes(
            telemetry_9d,
            human_empathy_intent_score=0.94,
        ),
    }
    results["success_criteria"] = _success_criteria(results)
    payload = {
        "metadata": {
            "engine": "energy_phase_engine.py",
            "version": VERSION,
            "seed": seed,
            "framework": "Materials & Energy Phase-Field Dynamics Diagnostic",
            "epistemic_status": "synthetic_research_model",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "simulation_results": results,
    }
    payload["provenance_sha256"] = CryptographicProvenanceLedger.generate_manifest(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Materials & Energy Phase-Field Dynamics Simulator"
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic random seed")
    parser.add_argument(
        "--output",
        type=str,
        default="energy_phase_audit.json",
        help="Output audit report path",
    )
    args = parser.parse_args()

    try:
        report = execute_energy_simulation(seed=args.seed)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] Energy phase-field simulation completed using seed {args.seed}.")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
        print(json.dumps(report["simulation_results"], indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] Simulation failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
