#!/usr/bin/env python3
"""Regression tests for astro_sync_engine.py."""

import math
import random
import unittest

from astro_sync_engine import (
    CryptographicProvenanceLedger,
    ElevenDimensionalObserver,
    RelativisticSyncEngine,
    execute_sync_simulation,
)


class AstroSyncEngineTests(unittest.TestCase):
    def test_stable_prediction(self):
        engine = RelativisticSyncEngine(base_light_lag_seconds=1.5, drift_tolerance=0.05)
        result = engine.predict_remote_state([1.0, 2.0], [0.001, -0.001], 3)
        self.assertEqual(result["vector_dimension"], 2)
        self.assertEqual(result["sync_stability_status"], "SYNCHRONIZED_STABLE")
        self.assertTrue(all(math.isfinite(value) for value in result["extrapolated_state_vector"]))

    def test_high_drift_warning(self):
        result = RelativisticSyncEngine(drift_tolerance=0.05).predict_remote_state(
            [1.0], [0.1], 3
        )
        self.assertEqual(result["sync_stability_status"], "HIGH_DRIFT_WARNING")

    def test_sync_rejects_invalid_vectors_and_ticks(self):
        engine = RelativisticSyncEngine()
        with self.assertRaises(ValueError):
            engine.predict_remote_state([1.0], [], 3)
        with self.assertRaises(ValueError):
            engine.predict_remote_state([math.nan], [0.1], 3)
        with self.assertRaises(ValueError):
            engine.predict_remote_state([1.0], [0.1], -1)

    def test_observer_requires_exact_9d_input(self):
        observer = ElevenDimensionalObserver()
        with self.assertRaises(ValueError):
            observer.calibrate_axes([0.1] * 8, 0.9)
        with self.assertRaises(ValueError):
            observer.calibrate_axes([0.1] * 9, 1.1)

    def test_reference_run_passes_success_gate(self):
        report = execute_sync_simulation(seed=42)
        self.assertTrue(report["simulation_results"]["success_criteria"]["overall_success"])

    def test_seeded_report_and_provenance_are_reproducible(self):
        first = execute_sync_simulation(seed=42)
        second = execute_sync_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_report(self):
        self.assertNotEqual(execute_sync_simulation(42), execute_sync_simulation(43))

    def test_global_random_state_is_not_consumed(self):
        random.seed(222)
        expected = random.random()
        random.seed(222)
        execute_sync_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
