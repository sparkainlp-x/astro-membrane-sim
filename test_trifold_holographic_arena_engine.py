#!/usr/bin/env python3
"""Regression tests for trifold_holographic_arena_engine.py."""

import math
import random
import unittest

from trifold_holographic_arena_engine import (
    CryptographicProvenanceLedger,
    ElevenDimensionalObserver,
    TikTakInfinityLoop,
    TrifoldSpinningArena,
    execute_trifold_arena_simulation,
)


class TrifoldArenaTests(unittest.TestCase):
    def test_three_membranes_have_normalized_phases(self):
        states = TrifoldSpinningArena(angular_velocity=1.5).rotate_arenas(5)
        self.assertEqual(len(states), 3)
        for state in states.values():
            self.assertGreaterEqual(state["phase_angle"], 0.0)
            self.assertLess(state["phase_angle"], 2.0 * math.pi)
            self.assertLessEqual(abs(state["yin_yang_balance"]), 1.0)

    def test_arena_rejects_invalid_ticks(self):
        with self.assertRaises(ValueError):
            TrifoldSpinningArena().rotate_arenas(-1)
        with self.assertRaises(ValueError):
            TrifoldSpinningArena().rotate_arenas(True)

    def test_observer_requires_nine_finite_values(self):
        observer = ElevenDimensionalObserver()
        with self.assertRaises(ValueError):
            observer.calibrate_observer_axes([0.1] * 8, 0.8)
        with self.assertRaises(ValueError):
            observer.calibrate_observer_axes([math.nan] + [0.1] * 8, 0.8)
        with self.assertRaises(ValueError):
            observer.calibrate_observer_axes([0.1] * 9, 1.1)

    def test_observer_reports_two_axes(self):
        result = ElevenDimensionalObserver().calibrate_observer_axes([0.2] * 9, 0.8)
        self.assertEqual(result["spatial_dimensions"], 9)
        self.assertEqual(result["observer_dimensions"], 2)
        self.assertEqual(result["social_proxy_status"], "ALIGNMENT_PROXY_PASS")

    def test_temporal_loop_is_measured(self):
        result = TikTakInfinityLoop.process_loop(0.45, 0.65, 0.82)
        self.assertAlmostEqual(result["loop_delta"], 0.37)
        self.assertTrue(math.isfinite(result["infinity_harmonic_resonance"]))
        self.assertEqual(result["loop_stability"], "STABLE_DIAGNOSTIC")

    def test_seeded_report_and_manifest_are_reproducible(self):
        first = execute_trifold_arena_simulation(seed=42)
        second = execute_trifold_arena_simulation(seed=42)
        self.assertEqual(first, second)
        self.assertEqual(
            first["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest({
                "metadata": first["metadata"],
                "simulation_results": first["simulation_results"],
            }),
        )

    def test_different_seed_changes_telemetry(self):
        first = execute_trifold_arena_simulation(seed=42)
        second = execute_trifold_arena_simulation(seed=43)
        self.assertNotEqual(first, second)

    def test_global_random_state_is_not_consumed(self):
        random.seed(100)
        expected = random.random()
        random.seed(100)
        execute_trifold_arena_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
