#!/usr/bin/env python3
"""Regression tests for wormhole_crystallization_engine.py."""

import math
import random
import unittest

from wormhole_crystallization_engine import (
    CryptographicProvenanceLedger,
    ElevenDimensionalObserver,
    TrifoldWormholeBridge,
    WormholeCrystallizationMembrane,
    execute_wormhole_simulation,
)


class WormholeCrystallizationTests(unittest.TestCase):
    def test_reference_throat_passes_without_pinch_off(self):
        membrane = WormholeCrystallizationMembrane(throat_radius=1.2)
        result = membrane.evaluate_throat_dynamics(0.75, 0.40)
        self.assertFalse(result["throat_pinch_off_risk"])
        self.assertGreaterEqual(result["adjusted_stability"], 0.0)

    def test_throat_rejects_invalid_inputs(self):
        membrane = WormholeCrystallizationMembrane()
        with self.assertRaises(ValueError):
            membrane.evaluate_throat_dynamics(-0.1, 0.4)
        with self.assertRaises(ValueError):
            membrane.evaluate_throat_dynamics(0.1, math.nan)
        with self.assertRaises(ValueError):
            WormholeCrystallizationMembrane(throat_radius=0.0)

    def test_bridge_resonance_is_explicitly_bounded(self):
        result = TrifoldWormholeBridge().transmit_across_throat(
            [0.1, 0.2], 0.68, [0.3, 0.4]
        )
        self.assertTrue(result["resonance_bounded"])
        self.assertLessEqual(
            abs(result["resonance_factor"]), result["resonance_bound"]
        )
        self.assertEqual(
            result["transmission_integrity"], "BOUNDED_SYNTHETIC_RESIDUAL"
        )

    def test_bridge_rejects_mismatched_packets(self):
        with self.assertRaises(ValueError):
            TrifoldWormholeBridge().transmit_across_throat([0.1], 0.5, [0.2, 0.3])

    def test_observer_requires_exactly_nine_values(self):
        observer = ElevenDimensionalObserver()
        with self.assertRaises(ValueError):
            observer.calibrate_axes([0.1] * 8, 0.9)
        with self.assertRaises(ValueError):
            observer.calibrate_axes([math.nan] + [0.1] * 8, 0.9)

    def test_seeded_report_and_provenance_are_reproducible(self):
        first = execute_wormhole_simulation(seed=42)
        second = execute_wormhole_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertTrue(first["simulation_results"]["success_criteria"]["overall_success"])
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_bridge_inputs(self):
        first = execute_wormhole_simulation(seed=42)
        second = execute_wormhole_simulation(seed=43)
        self.assertNotEqual(first, second)

    def test_global_random_state_is_not_consumed(self):
        random.seed(111)
        expected = random.random()
        random.seed(111)
        execute_wormhole_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
