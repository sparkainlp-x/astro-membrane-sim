#!/usr/bin/env python3
"""Regression tests for sparkainlp_master_engine.py."""

import math
import unittest

from sparkainlp_master_engine import (
    AntiCrystallizationEngine,
    HolographicMembraneMapper,
    RelativisticSyncPredictor,
    SelfKnowingCalibrator,
    deterministic_sha256,
    execute_master_simulation,
)


class MasterEngineTests(unittest.TestCase):
    def test_same_seed_is_reproducible(self):
        first = execute_master_simulation(seed=42)
        second = execute_master_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(deterministic_sha256(first), deterministic_sha256(second))

    def test_different_seed_changes_randomized_lanes(self):
        first = execute_master_simulation(seed=42)
        second = execute_master_simulation(seed=43)
        self.assertNotEqual(first, second)

    def test_mapper_rejects_nonfinite_values(self):
        with self.assertRaises(ValueError):
            HolographicMembraneMapper().compress_bulk([0.1, math.nan])

    def test_phase_engine_rejects_negative_gradient(self):
        with self.assertRaises(ValueError):
            AntiCrystallizationEngine().evaluate_free_energy(0.5, -0.1, 0.1)

    def test_sync_requires_matching_vector_lengths(self):
        with self.assertRaises(ValueError):
            RelativisticSyncPredictor().predict_telemetry([1.0], [], 1)

    def test_sync_rejects_negative_ticks(self):
        with self.assertRaises(ValueError):
            RelativisticSyncPredictor().predict_telemetry([1.0], [0.1], -1)

    def test_calibrator_rejects_nonfinite_uncertainty(self):
        with self.assertRaises(ValueError):
            SelfKnowingCalibrator().verify_invariants([1.0], math.inf)

    def test_master_report_contains_all_four_lanes(self):
        results = execute_master_simulation(seed=7)["simulation_results"]
        self.assertEqual(
            set(results),
            {
                "holographic_boundary",
                "phase_field_energy",
                "relativistic_sync_sample",
                "self_knowing_calibration",
            },
        )


if __name__ == "__main__":
    unittest.main()
