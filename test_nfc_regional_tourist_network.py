#!/usr/bin/env python3
"""Regression tests for nfc_regional_tourist_network.py."""

import math
import random
import unittest

from nfc_regional_tourist_network import (
    ElevenDimensionalObserver,
    RegionalNFCCoordinator,
    execute_regional_simulation,
)


class RegionalNFCTouristNetworkTests(unittest.TestCase):
    def test_reference_traffic_processes_all_waypoints(self):
        report = execute_regional_simulation(seed=42)
        traffic = report["simulation_results"]["regional_traffic_coordinator"]
        self.assertEqual(traffic["total_taps_processed"], 3)
        self.assertEqual(traffic["valid_waypoint_dispatch_count"], 3)
        self.assertEqual(traffic["network_status"], "SYNCHRONIZED_REGIONAL_ACTIVE")
        self.assertAlmostEqual(traffic["mean_educational_index"], 0.9466667, places=5)

    def test_each_event_is_identity_free_and_digest_bound(self):
        traffic = execute_regional_simulation(42)["simulation_results"]["regional_traffic_coordinator"]
        for event in traffic["waypoint_dispatch_logs"]:
            self.assertFalse(event["visitor_identity_collected"])
            self.assertEqual(len(event["anonymized_event_digest_sha256"]), 64)

    def test_unknown_waypoint_falls_back_explicitly(self):
        result = RegionalNFCCoordinator().simulate_regional_traffic([
            {"waypoint_id": "UNKNOWN", "intent_score": 0.8}
        ])
        self.assertEqual(result["valid_waypoint_dispatch_count"], 0)
        self.assertEqual(
            result["waypoint_dispatch_logs"][0]["tap_status"],
            "UNKNOWN_WAYPOINT_FALLBACK",
        )

    def test_invalid_events_fail_closed(self):
        coordinator = RegionalNFCCoordinator()
        with self.assertRaises(ValueError):
            coordinator.simulate_regional_traffic([{"waypoint_id": "WAYPOINT-FUNDY-TRAIL", "intent_score": 1.1}])
        with self.assertRaises(ValueError):
            coordinator.simulate_regional_traffic([{"waypoint_id": "WAYPOINT-FUNDY-TRAIL", "intent_score": math.nan}])
        with self.assertRaises(ValueError):
            coordinator.simulate_regional_traffic([{}])

    def test_observer_requires_exactly_nine_values(self):
        with self.assertRaises(ValueError):
            ElevenDimensionalObserver().calibrate_axes([0.1] * 8, 0.9)

    def test_reference_pipeline_passes_success_gate(self):
        report = execute_regional_simulation(seed=42)
        self.assertTrue(report["simulation_results"]["success_criteria"]["overall_success"])

    def test_seeded_report_is_reproducible(self):
        self.assertEqual(execute_regional_simulation(42), execute_regional_simulation(42))

    def test_global_random_state_is_not_consumed(self):
        random.seed(777)
        expected = random.random()
        random.seed(777)
        execute_regional_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
