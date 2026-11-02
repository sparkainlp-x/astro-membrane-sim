#!/usr/bin/env python3
"""Regression tests for orbital_phase_field_engine.py."""

import math
import unittest

from orbital_phase_field_engine import (
    OrbitalPhaseFieldEngine,
    deterministic_sha256,
    run_simulation_suite,
)


class OrbitalPhaseFieldEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = OrbitalPhaseFieldEngine()

    def test_free_energy_terms(self):
        result = self.engine.compute_free_energy(
            phi=0.5,
            gradient_norm_sq=0.04,
            crys_index=0.1,
        )
        self.assertAlmostEqual(result["double_well_potential"], 0.0625)
        self.assertAlmostEqual(result["crystallization_penalty"], 0.0085)
        self.assertAlmostEqual(result["total_free_energy"], 0.091)
        self.assertFalse(result["crystallization_locked"])

    def test_crystallization_threshold_locks(self):
        result = self.engine.compute_free_energy(
            phi=0.2,
            gradient_norm_sq=0.01,
            crys_index=0.21,
        )
        self.assertTrue(result["crystallization_locked"])
        self.assertEqual(result["engine_action"], "APPLY_FEEDBACK_DAMPING")

    def test_explicit_phase_threshold_is_reachable(self):
        result = self.engine.compute_free_energy(
            phi=0.8,
            gradient_norm_sq=0.01,
            crys_index=0.05,
        )
        self.assertTrue(result["crystallization_locked"])

    def test_invalid_values_fail_closed(self):
        invalid_cases = (
            {"phi": -0.01, "gradient_norm_sq": 0.1, "crys_index": 0.1},
            {"phi": 1.01, "gradient_norm_sq": 0.1, "crys_index": 0.1},
            {"phi": 0.5, "gradient_norm_sq": -0.1, "crys_index": 0.1},
            {"phi": 0.5, "gradient_norm_sq": 0.1, "crys_index": -0.1},
            {"phi": math.nan, "gradient_norm_sq": 0.1, "crys_index": 0.1},
            {"phi": 0.5, "gradient_norm_sq": math.inf, "crys_index": 0.1},
        )
        for case in invalid_cases:
            with self.subTest(case=case):
                with self.assertRaises(ValueError):
                    self.engine.compute_free_energy(**case)

    def test_same_seed_has_same_report_and_hash(self):
        first = run_simulation_suite(seed=42, steps=8)
        second = run_simulation_suite(seed=42, steps=8)
        self.assertEqual(first, second)
        self.assertEqual(deterministic_sha256(first), deterministic_sha256(second))

    def test_different_seed_changes_report(self):
        first = run_simulation_suite(seed=42, steps=5)
        second = run_simulation_suite(seed=43, steps=5)
        self.assertNotEqual(first, second)
        self.assertNotEqual(deterministic_sha256(first), deterministic_sha256(second))

    def test_zero_steps_is_valid(self):
        report = run_simulation_suite(seed=42, steps=0)
        self.assertEqual(report["trajectory"], [])

    def test_global_random_state_is_not_consumed(self):
        import random

        random.seed(1234)
        expected = random.random()
        random.seed(1234)
        run_simulation_suite(seed=42, steps=3)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
