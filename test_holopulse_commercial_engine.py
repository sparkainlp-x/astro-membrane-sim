#!/usr/bin/env python3
"""Regression tests for holopulse_commercial_engine.py."""

import hashlib
import math
import random
import unittest

from holopulse_commercial_engine import (
    CommercialLicenseProtector,
    HoloPulseCommercialDispatcher,
    RESEARCH_DEMO_TOKEN,
    execute_holopulse_simulation,
)


class HoloPulseCommercialTests(unittest.TestCase):
    def test_research_demo_license_is_explicit(self):
        protector = CommercialLicenseProtector()
        self.assertTrue(protector.verify_license())
        self.assertEqual(protector.status(), "RESEARCH_DEMO_LICENSE_VERIFIED")

    def test_external_digest_verification(self):
        token = "external-enterprise-token"
        digest = hashlib.sha256(token.encode()).hexdigest()
        protector = CommercialLicenseProtector(token, digest)
        self.assertTrue(protector.verify_license())
        self.assertEqual(protector.status(), "EXTERNAL_TOKEN_DIGEST_VERIFIED")

    def test_invalid_external_token_is_rejected(self):
        token = "external-enterprise-token"
        digest = hashlib.sha256(token.encode()).hexdigest()
        with self.assertRaises(PermissionError):
            execute_holopulse_simulation(
                license_token="wrong-token",
                authorized_token_sha256=digest,
            )

    def test_campaign_dispatch_and_synthetic_safety(self):
        result = HoloPulseCommercialDispatcher().dispatch_campaign(
            "AUTOMOTIVE_SHOWROOM", 24.5
        )
        self.assertEqual(result["target_asset"], "vehicle_model_rotation_3d")
        self.assertEqual(result["hardware_safety_status"], "SYNTHETIC_THERMAL_CHECK_PASS")
        self.assertFalse(result["hardware_command_issued"])
        self.assertFalse(result["customer_identity_collected"])

    def test_dispatch_rejects_unknown_mode_and_nonfinite_temperature(self):
        dispatcher = HoloPulseCommercialDispatcher()
        with self.assertRaises(ValueError):
            dispatcher.dispatch_campaign("UNKNOWN", 20.0)
        with self.assertRaises(ValueError):
            dispatcher.dispatch_campaign("BLACK_FRIDAY_FLASH", math.nan)

    def test_reference_run_passes_success_gate(self):
        report = execute_holopulse_simulation(seed=42)
        self.assertTrue(report["simulation_results"]["success_criteria"]["overall_success"])

    def test_seeded_report_is_reproducible(self):
        self.assertEqual(
            execute_holopulse_simulation(seed=42),
            execute_holopulse_simulation(seed=42),
        )

    def test_global_random_state_is_not_consumed(self):
        random.seed(999)
        expected = random.random()
        random.seed(999)
        execute_holopulse_simulation(seed=42)
        observed = random.random()
        self.assertEqual(observed, expected)


if __name__ == "__main__":
    unittest.main()
