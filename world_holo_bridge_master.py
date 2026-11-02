#!/usr/bin/env python3
"""
world_holo_bridge_master.py
--------------------------------------------------------------------------------
WorldHoloBridge: Master Spatial Computing & Synthetic Network Diagnostic
Copyright (c) 2026 Hicham JF Brisson / Spark AI NLP (sparkainlp-x)
License: AGPL-3.0-only

EPISTEMIC BOUNDARY & HONESTY CONTRACT:
- SYNTHETIC TESTBENCH: Composes regional NFC, wormhole, trifold-arena, and
  unified-domain diagnostics into one reproducible master report.
- NO HARDWARE CONTROL CLAIM: Does not access NFC tags, Wi-Fi, LED fans,
  displays, spacecraft, or physical infrastructure.
- NO PHYSICAL WORMHOLE CLAIM: Wormhole and tensor labels are software-level
  diagnostics only; no spacetime or information-transfer claim is made.
- DETERMINISM: Component reports use explicit seeds and timestamp-free
  canonical SHA-256 provenance.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import json
import math
import random

from nfc_regional_tourist_network import execute_regional_simulation
from sparkainlp_super_system import execute_super_system
from trifold_holographic_arena_engine import execute_trifold_arena_simulation
from wormhole_crystallization_engine import execute_wormhole_simulation

VERSION = "1.1.0"


def _canonical_hash(payload):
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def _finite(name, value):
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return value


class WorldHoloBridgeMasterCore:
    """Compose validated modules without mutating their source logic."""

    def __init__(self, seed=42):
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValueError("seed must be an integer.")
        self.seed = seed

    def execute_bridge_cycle(self):
        regional = execute_regional_simulation(seed=self.seed)
        wormhole = execute_wormhole_simulation(seed=self.seed)
        arena = execute_trifold_arena_simulation(seed=self.seed)
        unified = execute_super_system(seed=self.seed)

        regional_results = regional["simulation_results"]
        traffic = regional_results["regional_traffic_coordinator"]
        wormhole_results = wormhole["simulation_results"]
        arena_results = arena["simulation_results"]
        unified_results = unified["simulation_results"]

        # A private seeded choice represents an offline routing decision only.
        routing_rng = random.Random(self.seed)
        dispatch_log = traffic["waypoint_dispatch_logs"]
        active_index = routing_rng.randrange(len(dispatch_log))
        active_event = dispatch_log[active_index]
        throat = wormhole_results["wormhole_membrane_dynamics"]
        bridge = wormhole_results["trifold_bridge_transmission"]
        present = arena_results["trifold_spinning_membranes"]["PRESENT_MEMBRANE"]
        observer = regional_results["eleven_dimensional_calibration"]

        coupling_metrics = {
            "educational_index": _finite(
                "educational index", traffic["mean_educational_index"]
            ),
            "adjusted_throat_stability": _finite(
                "adjusted throat stability", throat["adjusted_stability"]
            ),
            "bridge_resonance": _finite(
                "bridge resonance", bridge["resonance_factor"]
            ),
            "present_membrane_balance": _finite(
                "present membrane balance", present["yin_yang_balance"]
            ),
            "unified_coupling_phase": _finite(
                "unified coupling phase", unified_results["coupling_metrics"]["energy_phase"]
            ),
        }
        criteria = {
            "regional_dispatch_active": active_event["tap_status"] == "DISPATCH_ACTIVE",
            "regional_privacy_gate_pass": all(
                log["visitor_identity_collected"] is False
                for log in dispatch_log
            ),
            "wormhole_throat_not_pinched": not throat["throat_pinch_off_risk"],
            "bridge_resonance_bounded": bridge["resonance_bounded"],
            "trifold_arena_gate_pass": arena_results["success_criteria"]["overall_success"],
            "unified_domain_gate_pass": unified_results["master_cycle_status"] == "HARMONIZED_SUPER_SYSTEM",
            "coupling_metrics_finite": all(math.isfinite(value) for value in coupling_metrics.values()),
            "observer_9_plus_2_present": (
                observer["spatial_dimensions"] == 9
                and observer["observer_dimensions"] == 2
            ),
        }
        return {
            "master_bridge_status": (
                "WORLD_BRIDGE_HARMONIZED" if all(criteria.values())
                else "RECALIBRATION_TRIGGERED"
            ),
            "regional_nfc_dispatch": {
                "active_waypoint": active_event["waypoint_id"],
                "target_hologram_asset": active_event["target_asset"],
                "synthetic_target_rpm": active_event["synthetic_target_rpm"],
                "routing_status": active_event["tap_status"],
            },
            "wormhole_tensor_dynamics": {
                "crystallization_index": throat["crystallization_index"],
                "adjusted_throat_stability": throat["adjusted_stability"],
                "throat_pinch_off_risk": throat["throat_pinch_off_risk"],
                "bridge_resonance": bridge["resonance_factor"],
                "bridge_resonance_bounded": bridge["resonance_bounded"],
            },
            "trifold_arena_state": {
                "present_membrane_phase": present["phase_angle"],
                "present_membrane_yin_yang": present["yin_yang_balance"],
            },
            "eleven_dimensional_observer": observer,
            "coupling_metrics": coupling_metrics,
            "success_criteria": {
                "criteria": criteria,
                "overall_success": all(criteria.values()),
            },
            "epistemic_label": "BOUNDED_SYNTHETIC_WORLD_HOLO_BRIDGE",
        }


def execute_world_holo_bridge(seed=42):
    core = WorldHoloBridgeMasterCore(seed=seed)
    cycle = core.execute_bridge_cycle()
    # Re-run component reports only to bind their exact provenance hashes into
    # the master manifest; all components are deterministic and timestamp-free.
    components = {
        "regional_nfc": execute_regional_simulation(seed=seed),
        "wormhole": execute_wormhole_simulation(seed=seed),
        "trifold_arena": execute_trifold_arena_simulation(seed=seed),
        "unified_super_system": execute_super_system(seed=seed),
    }
    payload = {
        "metadata": {
            "engine": "world_holo_bridge_master.py",
            "version": VERSION,
            "seed": seed,
            "framework": "WorldHoloBridge master synthetic diagnostic",
            "epistemic_status": "synthetic_research_model",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "simulation_results": cycle,
        "component_provenance": {
            name: report["provenance_sha256"] for name, report in components.items()
        },
    }
    payload["provenance_sha256"] = _canonical_hash(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(description="WorldHoloBridge Master Diagnostic")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed")
    parser.add_argument("--output", type=str, default="world_holo_bridge_audit.json", help="Output path")
    args = parser.parse_args()
    try:
        report = execute_world_holo_bridge(seed=args.seed)
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] WorldHoloBridge cycle completed using seed {args.seed}.")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
        print(json.dumps(report["simulation_results"], indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"[ERROR] WorldHoloBridge failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
