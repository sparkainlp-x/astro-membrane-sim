#!/usr/bin/env python3
"""Regression tests for world_holo_bridge_master.py."""

import math
import random
import unittest

from world_holo_bridge_master import (
    WorldHoloBridgeMasterCore,
    execute_world_holo_bridge,
)


class WorldHoloBridgeTests(unittest.TestCase):
    def test_reference_cycle_harmonizes(self):
        report = execute_world_holo_bridge(seed=42)
        results = report["simulation_results"]
        self.assertEqual(results["master_bridge_status"], "WORLD_BRIDGE_HARMONIZED")
        self.assertTrue(results["success_criteria"]["overall_success"])
        self.assertTrue(all(results["success_criteria"]["criteria"].values()))

    def test_required_domains_are_composed(self):
        report = execute_world_holo_bridge(seed=42)
        self.assertEqual(
            set(report["component_provenance"]),
            {"regional_nfc", "wormhole", "trifold_arena", "unified_super_system"},
        )
        results = report["simulation_results"]
        self.assertIn("regional_nfc_dispatch", results)
        self.assertIn("wormhole_tensor_dynamics", results)
        self.assertIn("trifold_arena_state", results)
        self.assertIn("eleven_dimensional_observer", results)

    def test_coupling_metrics_are_finite(self):
        metrics = execute_world_holo_bridge(42)["simulation_results"]["coupling_metrics"]
        self.assertTrue(all(math.isfinite(value) for value in metrics.values()))

    def test_seeded_report_is_reproducible(self):
        self.assertEqual(execute_world_holo_bridge(42), execute_world_holo_bridge(42))

    def test_different_seed_changes_report(self):
        self.assertNotEqual(execute_world_holo_bridge(42), execute_world_holo_bridge(43))

    def test_invalid_seed_fails_closed(self):
        with self.assertRaises(ValueError):
            WorldHoloBridgeMasterCore(seed=True)

    def test_global_random_state_is_not_consumed(self):
        random.seed(888)
        expected = random.random()
        random.seed(888)
        execute_world_holo_bridge(42)
        observed = random.random()
        self.assertEqual(observed, expected)

    def test_no_hardware_or_runtime_self_rewrite_claim(self):
        report = execute_world_holo_bridge(42)
        self.assertEqual(
            report["simulation_results"]["epistemic_label"],
            "BOUNDED_SYNTHETIC_WORLD_HOLO_BRIDGE",
        )


if __name__ == "__main__":
    unittest.main()
