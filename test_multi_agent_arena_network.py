#!/usr/bin/env python3
"""
Regression Test Suite: Multi-Agent Trifold Arena & Synthetic Tensor Network
"""

import math
import random
import unittest

from multi_agent_arena_network import (
    CryptographicProvenanceLedger,
    HolographicArenaNode,
    WormholeTensorNetwork,
    execute_multi_agent_simulation,
)


class TestMultiAgentArenaNetwork(unittest.TestCase):
    def test_node_state_computation(self):
        node = HolographicArenaNode("Test-Node", angular_velocity=1.2)
        telemetry = [0.5, 0.6, 0.7, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        report = node.compute_node_state(tick_count=2, local_telemetry=telemetry)
        self.assertEqual(report["node_id"], "Test-Node")
        self.assertIn("PAST_MEMBRANE", report["membrane_states"])
        self.assertIn("PRESENT_MEMBRANE", report["membrane_states"])
        self.assertIn("FUTURE_MEMBRANE", report["membrane_states"])
        self.assertEqual(report["node_status"], "SYNCHRONIZED_ACTIVE")
        self.assertAlmostEqual(report["d11_empathy_alignment"], 0.93, places=2)

    def test_tensor_network_bridging(self):
        network = WormholeTensorNetwork(damping_gain=0.85)
        mock_states = [
            {"d10_self_knowing": 0.5, "d11_empathy_alignment": 0.9},
            {"d10_self_knowing": 0.6, "d11_empathy_alignment": 0.95},
        ]
        bridge_res = network.bridge_nodes(mock_states)
        self.assertEqual(
            bridge_res["tensor_network_bridge"],
            "ACTIVE_EINSTEIN_ROSEN_MULTINODE",
        )
        self.assertIn("collective_resonance", bridge_res)
        self.assertIn("crystallization_lock_risk", bridge_res)

    def test_deterministic_reproducibility(self):
        report_a = execute_multi_agent_simulation(seed=42, node_count=3)
        report_b = execute_multi_agent_simulation(seed=42, node_count=3)
        self.assertEqual(report_a, report_b)
        self.assertEqual(report_a["provenance_sha256"], report_b["provenance_sha256"])
        self.assertEqual(
            report_a["simulation_results"]["active_node_count"],
            report_b["simulation_results"]["active_node_count"],
        )

    def test_seed_variance(self):
        report_42 = execute_multi_agent_simulation(seed=42, node_count=3)
        report_100 = execute_multi_agent_simulation(seed=100, node_count=3)
        self.assertNotEqual(report_42["provenance_sha256"], report_100["provenance_sha256"])

    def test_manifest_matches_payload(self):
        report = execute_multi_agent_simulation(seed=42, node_count=3)
        payload = {
            "metadata": report["metadata"],
            "simulation_results": report["simulation_results"],
        }
        self.assertEqual(
            report["provenance_sha256"],
            CryptographicProvenanceLedger.generate_manifest(payload),
        )

    def test_node_requires_nine_finite_values(self):
        node = HolographicArenaNode("Test-Node")
        with self.assertRaises(ValueError):
            node.compute_node_state(2, [0.1] * 8)
        with self.assertRaises(ValueError):
            node.compute_node_state(2, [math.nan] + [0.1] * 8)

    def test_network_rejects_empty_states_and_invalid_count(self):
        with self.assertRaises(ValueError):
            WormholeTensorNetwork().bridge_nodes([])
        with self.assertRaises(ValueError):
            execute_multi_agent_simulation(seed=42, node_count=0)

    def test_global_random_state_is_not_consumed(self):
        random.seed(555)
        expected = random.random()
        random.seed(555)
        execute_multi_agent_simulation(seed=42, node_count=3)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
