#!/usr/bin/env python3
"""Regression tests for spinning_cascade_engine.py."""

import math
import random
import unittest

from spinning_cascade_engine import (
    CryptographicProvenanceLedger,
    SpinningCascadeSimulator,
    SpinningMembraneArray,
    execute_spinning_cascade_simulation,
)


class SpinningCascadeEngineTests(unittest.TestCase):
    def test_rotational_potential_energy_is_computed(self):
        simulator = SpinningCascadeSimulator(angular_velocity=2.0, cascade_threshold=1.0)
        result = simulator.evaluate_node_cascade(0.2, 0.5)
        self.assertAlmostEqual(result["rotational_potential_energy"], 0.5)
        self.assertAlmostEqual(result["effective_energy"], 0.7)
        self.assertFalse(result["cascade_triggered"])

    def test_threshold_triggers_cascade(self):
        simulator = SpinningCascadeSimulator(angular_velocity=2.0, cascade_threshold=0.7)
        result = simulator.evaluate_node_cascade(0.2, 0.5)
        self.assertTrue(result["cascade_triggered"])
        self.assertAlmostEqual(result["cascade_intensity"], 0.0)

    def test_invalid_node_inputs_fail_closed(self):
        simulator = SpinningCascadeSimulator()
        with self.assertRaises(ValueError):
            simulator.evaluate_node_cascade(-0.1, 0.2)
        with self.assertRaises(ValueError):
            simulator.evaluate_node_cascade(0.1, math.nan)

    def test_ring_requires_private_rng(self):
        array = SpinningMembraneArray(node_count=2)
        with self.assertRaises(TypeError):
            array.simulate_rotation_ring(SpinningCascadeSimulator(), random)

    def test_seeded_report_is_reproducible(self):
        first = execute_spinning_cascade_simulation(seed=42)
        second = execute_spinning_cascade_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_ring_telemetry(self):
        first = execute_spinning_cascade_simulation(seed=42)
        second = execute_spinning_cascade_simulation(seed=43)
        self.assertNotEqual(first, second)

    def test_global_random_state_is_not_consumed(self):
        random.seed(99)
        expected = random.random()
        random.seed(99)
        execute_spinning_cascade_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)

    def test_empty_ring_has_zero_active_fraction(self):
        array = SpinningMembraneArray(node_count=0)
        telemetry = array.simulate_rotation_ring(
            SpinningCascadeSimulator(), random.Random(42)
        )
        self.assertEqual(telemetry, [])


if __name__ == "__main__":
    unittest.main()
