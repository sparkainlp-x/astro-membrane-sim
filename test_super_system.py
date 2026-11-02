#!/usr/bin/env python3
"""Regression tests for sparkainlp_super_system.py."""

import math
import random
import unittest

from sparkainlp_super_system import (
    UnifiedSuperSystemDispatcher,
    deterministic_sha256,
    execute_super_system,
)


class SuperSystemTests(unittest.TestCase):
    def test_reference_cycle_harmonizes(self):
        cycle = UnifiedSuperSystemDispatcher(seed=42).execute_master_cycle()
        self.assertEqual(cycle["master_cycle_status"], "HARMONIZED_SUPER_SYSTEM")
        self.assertTrue(all(cycle["coupling_criteria"].values()))

    def test_all_component_domains_are_present(self):
        cycle = UnifiedSuperSystemDispatcher(seed=42).execute_master_cycle()
        self.assertEqual(
            set(cycle["component_success"]),
            {"aerospace_sync", "energy_phase", "trifold_arena", "wormhole_diagnostic"},
        )
        self.assertEqual(len(cycle["coupling_metrics"]), 5)

    def test_adaptive_parameters_are_finite_and_bounded(self):
        cycle = UnifiedSuperSystemDispatcher(seed=42).execute_master_cycle()
        for value in cycle["adaptive_parameters"].values():
            self.assertTrue(math.isfinite(value))
        self.assertGreater(cycle["adaptive_parameters"]["mobility_scale"], 0.0)

    def test_seeded_report_and_provenance_are_reproducible(self):
        first = execute_super_system(seed=42)
        second = execute_super_system(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(first["provenance_sha256"], deterministic_sha256({
            "metadata": first["metadata"],
            "simulation_results": first["simulation_results"],
            "component_provenance": first["component_provenance"],
        }))

    def test_different_seed_changes_report(self):
        self.assertNotEqual(execute_super_system(42), execute_super_system(43))

    def test_invalid_seed_fails_closed(self):
        with self.assertRaises(ValueError):
            UnifiedSuperSystemDispatcher(seed=True)

    def test_global_random_state_is_not_consumed(self):
        random.seed(444)
        expected = random.random()
        random.seed(444)
        execute_super_system(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)

    def test_no_runtime_self_rewriting_is_reported(self):
        report = execute_super_system(seed=42)
        self.assertEqual(
            report["simulation_results"]["epistemic_label"],
            "BOUNDED_SYNTHETIC_CROSS_DOMAIN_ORCHESTRATOR",
        )


if __name__ == "__main__":
    unittest.main()
