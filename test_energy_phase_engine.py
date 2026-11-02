#!/usr/bin/env python3
"""Regression tests for energy_phase_engine.py."""

import math
import random
import unittest

from energy_phase_engine import (
    CentrifugalDampingSurrogate,
    CryptographicProvenanceLedger,
    ElevenDimensionalObserver,
    EnergyPhaseFieldSimulator,
    execute_energy_simulation,
)


class EnergyPhaseEngineTests(unittest.TestCase):
    def test_explicit_noise_step_is_repeatable_and_bounded(self):
        simulator = EnergyPhaseFieldSimulator()
        first = simulator.step_phase_evolution(
            0.35, 0.04, 0.12, noise=0.01, rotational_damping=0.001
        )
        second = simulator.step_phase_evolution(
            0.35, 0.04, 0.12, noise=0.01, rotational_damping=0.001
        )
        self.assertEqual(first, second)
        self.assertGreaterEqual(first["phi_updated"], 0.0)
        self.assertLessEqual(first["phi_updated"], 1.0)

    def test_phase_validation_fails_closed(self):
        simulator = EnergyPhaseFieldSimulator()
        with self.assertRaises(ValueError):
            simulator.step_phase_evolution(math.nan, 0.04, 0.12)
        with self.assertRaises(ValueError):
            simulator.step_phase_evolution(0.35, -0.04, 0.12)
        with self.assertRaises(ValueError):
            simulator.step_phase_evolution(0.35, 0.04, 0.12, dt=0.0)

    def test_rotational_surrogate_is_explicit(self):
        result = CentrifugalDampingSurrogate(
            angular_velocity=2.0, radius=0.5, damping_gain=0.1
        ).compute()
        self.assertAlmostEqual(result["rotational_potential_energy"], 0.5)
        self.assertAlmostEqual(result["damping_surrogate"], 0.05)
        self.assertEqual(
            result["epistemic_label"], "SCALAR_ROTATIONAL_DAMPING_SURROGATE"
        )

    def test_observer_requires_nine_values(self):
        with self.assertRaises(ValueError):
            ElevenDimensionalObserver().calibrate_axes([0.1] * 8, 0.9)

    def test_reference_run_passes_success_gate(self):
        report = execute_energy_simulation(seed=42)
        self.assertTrue(report["simulation_results"]["success_criteria"]["overall_success"])

    def test_seeded_report_and_provenance_are_reproducible(self):
        first = execute_energy_simulation(seed=42)
        second = execute_energy_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_report(self):
        self.assertNotEqual(execute_energy_simulation(42), execute_energy_simulation(43))

    def test_global_random_state_is_not_consumed(self):
        random.seed(333)
        expected = random.random()
        random.seed(333)
        execute_energy_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
