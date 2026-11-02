#!/usr/bin/env python3
"""Regression tests for sparkainlp_advanced_science_engine.py."""

import math
import random
import unittest

from sparkainlp_advanced_science_engine import (
    CryptographicProvenanceLedger,
    HolographicComplexityAnalyzer,
    StochasticPhaseFieldSimulator,
    execute_advanced_simulation,
)


class AdvancedScienceEngineTests(unittest.TestCase):
    def test_explicit_noise_step_is_repeatable(self):
        simulator = StochasticPhaseFieldSimulator()
        first = simulator.step_evolution(0.25, 0.04, 0.1, noise=0.02)
        second = simulator.step_evolution(0.25, 0.04, 0.1, noise=0.02)
        self.assertEqual(first, second)
        self.assertGreaterEqual(first["phi_updated"], 0.0)
        self.assertLessEqual(first["phi_updated"], 1.0)

    def test_invalid_phase_inputs_fail_closed(self):
        simulator = StochasticPhaseFieldSimulator()
        with self.assertRaises(ValueError):
            simulator.step_evolution(math.nan, 0.04, 0.1)
        with self.assertRaises(ValueError):
            simulator.step_evolution(0.25, -0.04, 0.1)
        with self.assertRaises(ValueError):
            simulator.step_evolution(0.25, 0.04, 0.1, dt=0.0)

    def test_complexity_rejects_negative_bulk_values(self):
        with self.assertRaises(ValueError):
            HolographicComplexityAnalyzer().compute_boundary_complexity([0.1, -0.2])

    def test_complexity_output_is_finite(self):
        result = HolographicComplexityAnalyzer(cell_width=2).compute_boundary_complexity(
            [0.1, 0.2, 0.3]
        )
        self.assertEqual(len(result["boundary_nodes"]), 2)
        self.assertTrue(math.isfinite(result["holographic_complexity_score"]))

    def test_seeded_advanced_report_is_reproducible(self):
        first = execute_advanced_simulation(seed=42, iterations=4)
        second = execute_advanced_simulation(seed=42, iterations=4)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_report(self):
        first = execute_advanced_simulation(seed=42, iterations=3)
        second = execute_advanced_simulation(seed=43, iterations=3)
        self.assertNotEqual(first, second)

    def test_global_random_state_is_not_consumed(self):
        random.seed(77)
        expected = random.random()
        random.seed(77)
        execute_advanced_simulation(seed=42, iterations=3)
        observed = random.random()
        self.assertEqual(observed, expected)

    def test_zero_iterations_is_valid(self):
        report = execute_advanced_simulation(seed=42, iterations=0)
        self.assertEqual(report["simulation_results"]["stochastic_phase_trajectory"], [])


if __name__ == "__main__":
    unittest.main()
