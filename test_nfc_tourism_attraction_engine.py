#!/usr/bin/env python3
"""Regression tests for nfc_tourism_attraction_engine.py."""

import math
import random
import unittest

from nfc_tourism_attraction_engine import (
    ElevenDimensionalObserver,
    NFCTourismWaypointRouter,
    execute_nfc_tourism_pipeline,
    _canonical_hash,
)


class NFCTourismAttractionTests(unittest.TestCase):
    def test_known_waypoint_dispatches_profile(self):
        result = NFCTourismWaypointRouter().process_nfc_tap(
            "WAYPOINT-FUNDY-TRAIL", 0.95
        )
        self.assertEqual(result["waypoint_dispatch_status"], "DISPATCH_SUCCESS")
        self.assertEqual(result["resolved_exhibit_theme"], "Geological Tectonic Shift")
        self.assertEqual(result["target_hologram_asset"], "tidal_basin_model")
        self.assertFalse(result["visitor_identity_collected"])
        self.assertEqual(len(result["anonymized_event_digest_sha256"]), 64)

    def test_unknown_waypoint_uses_explicit_fallback(self):
        result = NFCTourismWaypointRouter().process_nfc_tap("UNKNOWN", 0.8)
        self.assertEqual(result["waypoint_dispatch_status"], "DEFAULT_FALLBACK_ACTIVE")
        self.assertEqual(result["target_hologram_asset"], "default_logo_3d")

    def test_router_rejects_invalid_intent(self):
        router = NFCTourismWaypointRouter()
        with self.assertRaises(ValueError):
            router.process_nfc_tap("WAYPOINT-FUNDY-TRAIL", 1.1)
        with self.assertRaises(ValueError):
            router.process_nfc_tap("WAYPOINT-FUNDY-TRAIL", math.nan)

    def test_observer_requires_exactly_nine_values(self):
        with self.assertRaises(ValueError):
            ElevenDimensionalObserver().calibrate_axes([0.1] * 8, 0.9)
        with self.assertRaises(ValueError):
            ElevenDimensionalObserver().calibrate_axes([math.nan] + [0.1] * 8, 0.9)

    def test_reference_pipeline_passes_success_gate(self):
        report = execute_nfc_tourism_pipeline(seed=42)
        self.assertTrue(report["simulation_results"]["success_criteria"]["overall_success"])

    def test_seeded_report_is_reproducible(self):
        first = execute_nfc_tourism_pipeline(seed=42)
        second = execute_nfc_tourism_pipeline(seed=42)
        self.assertEqual(first, second)
        payload = {
            "metadata": first["metadata"],
            "simulation_results": first["simulation_results"],
        }
        self.assertEqual(first["provenance_sha256"], _canonical_hash(payload))

    def test_different_seed_changes_telemetry_report(self):
        self.assertNotEqual(
            execute_nfc_tourism_pipeline(seed=42),
            execute_nfc_tourism_pipeline(seed=43),
        )

    def test_global_random_state_is_not_consumed(self):
        random.seed(666)
        expected = random.random()
        random.seed(666)
        execute_nfc_tourism_pipeline(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
