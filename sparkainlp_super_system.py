#!/usr/bin/env python3
"""
sparkainlp_super_system.py
--------------------------------------------------------------------------------
Unified Research Orchestrator: Four Breakouts & Wormhole Diagnostic Protocol
Copyright (c) 2026 Hicham JF Brisson / Spark AI NLP (sparkainlp-x)
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC RESEARCH TESTBENCH: Composes validated aerospace, energy,
  trifold-arena, and wormhole diagnostic engines into one audit cycle.
- NO PHYSICAL CONTROL CLAIM: The coupling metrics are software-defined
  surrogates, not a physical metric tensor, spacetime model, or governance proof.
- NO RUNTIME SELF-REWRITING: Adaptive values are reported as deterministic
  parameters; source code and executable logic are never modified at runtime.
- DETERMINISM: Component reports, coupling metrics, and provenance are derived
  from explicit seeds and timestamp-free canonical JSON.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math

from astro_sync_engine import execute_sync_simulation
from energy_phase_engine import execute_energy_simulation
from trifold_holographic_arena_engine import execute_trifold_arena_simulation
from wormhole_crystallization_engine import execute_wormhole_simulation

VERSION = "4.0.1"


def canonical_json_bytes(payload):
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def deterministic_sha256(payload):
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _finite(name, value):
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return value


class UnifiedSuperSystemDispatcher:
    """Compose validated breakout reports without mutating their source logic."""

    def __init__(self, seed=42):
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError("seed must be an integer.")
        self.seed = seed

    def execute_master_cycle(self):
        sync_report = execute_sync_simulation(seed=self.seed)
        energy_report = execute_energy_simulation(seed=self.seed)
        arena_report = execute_trifold_arena_simulation(seed=self.seed)
        wormhole_report = execute_wormhole_simulation(seed=self.seed)

        sync = sync_report["simulation_results"]
        energy = energy_report["simulation_results"]
        arena = arena_report["simulation_results"]
        wormhole = wormhole_report["simulation_results"]

        sync_drift = _finite(
            "sync drift", sync["relativistic_sync_dynamics"]["max_velocity_drift"]
        )
        phase = _finite(
            "phase", energy["phase_field_dynamics"]["phi_updated"]
        )
        throat = _finite(
            "throat stability", wormhole["wormhole_membrane_dynamics"]["adjusted_stability"]
        )
        bridge = _finite(
            "bridge resonance", wormhole["trifold_bridge_transmission"]["resonance_factor"]
        )
        empathy_proxy = _finite(
            "empathy proxy",
            arena["eleven_dimensional_calibration"]["d11_empathetic_alignment_proxy"],
        )

        # Deterministic cross-domain summaries. These are coupling metrics, not
        # a physical tensor or a validated causal feedback law.
        adaptive_parameters = {
            "mobility_scale": 1.0 / (1.0 + abs(sync_drift)),
            "damping_scale": 1.0 + max(0.0, throat),
            "phase_alignment_score": 1.0 - abs(phase - 0.5),
            "bridge_resonance_abs": abs(bridge),
        }
        component_success = {
            "aerospace_sync": sync["success_criteria"]["overall_success"],
            "energy_phase": energy["success_criteria"]["overall_success"],
            "trifold_arena": arena["success_criteria"]["overall_success"],
            "wormhole_diagnostic": wormhole["success_criteria"]["overall_success"],
        }
        coupling_criteria = {
            "all_component_gates_pass": all(component_success.values()),
            "coupling_metrics_finite": all(
                math.isfinite(value) for value in adaptive_parameters.values()
            ),
            "observer_alignment_proxy_pass": empathy_proxy >= 0.70,
            "bridge_resonance_bounded": (
                wormhole["trifold_bridge_transmission"]["resonance_bounded"]
            ),
            "arena_membranes_complete": (
                len(arena["trifold_spinning_membranes"]) == 3
            ),
        }
        return {
            "master_cycle_status": (
                "HARMONIZED_SUPER_SYSTEM"
                if all(coupling_criteria.values())
                else "RECALIBRATION_TRIGGERED"
            ),
            "component_success": component_success,
            "coupling_metrics": {
                "sync_drift": sync_drift,
                "energy_phase": phase,
                "wormhole_adjusted_stability": throat,
                "bridge_resonance": bridge,
                "arena_empathy_proxy": empathy_proxy,
            },
            "adaptive_parameters": adaptive_parameters,
            "coupling_criteria": coupling_criteria,
            "epistemic_label": "BOUNDED_SYNTHETIC_CROSS_DOMAIN_ORCHESTRATOR",
        }


def execute_super_system(seed=42):
    dispatcher = UnifiedSuperSystemDispatcher(seed=seed)
    cycle = dispatcher.execute_master_cycle()
    component_reports = {
        "astro_sync": execute_sync_simulation(seed=seed),
        "energy_phase": execute_energy_simulation(seed=seed),
        "trifold_arena": execute_trifold_arena_simulation(seed=seed),
        "wormhole": execute_wormhole_simulation(seed=seed),
    }
    payload = {
        "metadata": {
            "engine": "sparkainlp_super_system.py",
            "version": VERSION,
            "seed": seed,
            "framework": "Unified four-breakout and wormhole orchestrator",
            "epistemic_status": "synthetic_research_model",
            "determinism": "timestamp excluded; component seeds explicit",
        },
        "simulation_results": cycle,
        "component_provenance": {
            name: report["provenance_sha256"]
            for name, report in component_reports.items()
        },
    }
    payload["provenance_sha256"] = deterministic_sha256(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(
        description="Spark AI NLP Unified Synthetic Research Orchestrator"
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed")
    parser.add_argument(
        "--output",
        type=str,
        default="super_system_audit.json",
        help="Output audit report path",
    )
    args = parser.parse_args()

    try:
        report = execute_super_system(seed=args.seed)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] Unified super-system cycle completed using seed {args.seed}.")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
        print(json.dumps(report["simulation_results"], indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError) as error:
        print(f"[ERROR] Super-system execution failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
