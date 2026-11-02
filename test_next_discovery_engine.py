#!/usr/bin/env python3
"""Regression tests for sparkainlp_next_discovery_engine.py."""

import math
import random
import unittest

from sparkainlp_next_discovery_engine import (
    CryptographicProvenanceLedger,
    EntropicInformationFlux,
    HolographicRenormalizationFlow,
    TopologicalGaugeDamping,
    execute_next_discovery_simulation,
)


class NextDiscoveryEngineTests(unittest.TestCase):
    def test_rg_flow_is_deterministic_and_validated(self):
        flow = HolographicRenormalizationFlow()
        first = flow.evolve_coupling(0.42, 0.85)
        second = flow.evolve_coupling(0.42, 0.85)
        self.assertEqual(first, second)
        with self.assertRaises(ValueError):
            flow.evolve_coupling(-0.1, 0.85)
        with self.assertRaises(ValueError):
            flow.evolve_coupling(0.42, 0.85, dt=0.0)

    def test_entropy_empty_and_invalid_inputs(self):
        engine = EntropicInformationFlux()
        empty = engine.compute_wedge_entropy([])
        self.assertEqual(empty["capacity_bound"], 0.0)
        self.assertEqual(empty["flux_efficiency"], 0.0)
        with self.assertRaises(ValueError):
            engine.compute_wedge_entropy([math.nan])
        with self.assertRaises(ValueError):
            engine.compute_wedge_entropy([-0.1])

    def test_gauge_lock_risk_is_explicit(self):
        engine = TopologicalGaugeDamping(gauge_coupling=0.35, lock_threshold=0.05)
        warning = engine.apply_gauge_correction(0.05, 0.0)
        self.assertTrue(warning["lock_risk"])
        self.assertFalse(warning["topological_lock_mitigated"])
        self.assertEqual(warning["action"], "VORTEX_ARREST_WARNING")

    def test_gauge_rejects_nonfinite_values(self):
        with self.assertRaises(ValueError):
            TopologicalGaugeDamping().apply_gauge_correction(math.inf, 0.1)

    def test_seeded_report_and_manifest_are_reproducible(self):
        first = execute_next_discovery_simulation(seed=42)
        second = execute_next_discovery_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "discovery_results": first["discovery_results"],
            }),
        )

    def test_different_seed_changes_entropy_lane(self):
        first = execute_next_discovery_simulation(seed=42)
        second = execute_next_discovery_simulation(seed=43)
        self.assertNotEqual(first, second)
        self.assertNotEqual(
            first["discovery_results"]["entropic_information_flux"],
            second["discovery_results"]["entropic_information_flux"],
        )

    def test_global_random_state_is_not_consumed(self):
        random.seed(88)
        expected = random.random()
        random.seed(88)
        execute_next_discovery_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
