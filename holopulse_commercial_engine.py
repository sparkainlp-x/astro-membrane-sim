#!/usr/bin/env python3
"""
holopulse_commercial_engine.py
--------------------------------------------------------------------------------
HoloPulse: Commercial Retail & Hospitality Dispatch Research Diagnostic
Copyright (c) 2026 Hicham JF Brisson / Spark AI NLP (sparkainlp-x)
License: AGPL-3.0-only

COMMERCIAL PROTECTION & EPISTEMIC NOTICE:
- The public research-demo token is for reproducible tests only. It is not a
  commercial entitlement and cannot protect proprietary code.
- Actual commercial verification requires an externally supplied expected
  SHA-256 digest or a separate signed-license service; none is bundled here.
- SYNTHETIC TESTBENCH: Campaign scheduling, thermal calculations, and telemetry
  are numerical surrogates only. No hardware command is issued.
- PRIVACY: No customer identity or personal data is accepted or logged.
- DETERMINISM: Runtime timestamps are excluded and a private seeded RNG is used.
--------------------------------------------------------------------------------
"""

import argparse
import hashlib
import hmac
import json
import math
import random
from numbers import Real

VERSION = "1.1.0"
RESEARCH_DEMO_TOKEN = "SPARK-AI-NLP-RESEARCH-DEMO"
CAMPAIGN_REGISTRY = {
    "AUTOMOTIVE_SHOWROOM": {
        "asset": "vehicle_model_rotation_3d",
        "target_rpm": 700,
        "priority": "HIGH",
    },
    "BLACK_FRIDAY_FLASH": {
        "asset": "holiday_promotional_burst_3d",
        "target_rpm": 750,
        "priority": "CRITICAL",
    },
    "HOSPITALITY_SEASONAL": {
        "asset": "dining_ambiance_thematic_3d",
        "target_rpm": 620,
        "priority": "STANDARD",
    },
}


def _finite_real(name, value):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number; got {value!r}.")
    return float(value)


def _hash(payload):
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


class CommercialLicenseProtector:
    """Verify a supplied token against an externally configured digest.

    With no expected digest, only the public research-demo token is accepted.
    This is intentionally not presented as commercial IP protection.
    """

    def __init__(self, license_token=None, authorized_token_sha256=None):
        self.token = RESEARCH_DEMO_TOKEN if license_token is None else license_token
        if not isinstance(self.token, str) or not self.token:
            raise ValueError("license_token must be a non-empty string.")
        self.is_research_demo = (
            license_token is None or self.token == RESEARCH_DEMO_TOKEN
        )
        self.authorized_hash = (
            authorized_token_sha256
            if authorized_token_sha256 is not None
            else _hash_text(RESEARCH_DEMO_TOKEN)
        )
        if not isinstance(self.authorized_hash, str) or len(self.authorized_hash) != 64:
            raise ValueError("authorized_token_sha256 must be a 64-character hex digest.")
        try:
            int(self.authorized_hash, 16)
        except ValueError as error:
            raise ValueError("authorized_token_sha256 must be hexadecimal.") from error

    def verify_license(self):
        candidate = _hash_text(self.token)
        return hmac.compare_digest(candidate, self.authorized_hash)

    def status(self):
        return (
            "RESEARCH_DEMO_LICENSE_VERIFIED"
            if self.is_research_demo
            else "EXTERNAL_TOKEN_DIGEST_VERIFIED"
        )


def _hash_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class HoloPulseCommercialDispatcher:
    """Resolve campaign profiles and compute synthetic thermal/power diagnostics."""

    def __init__(self, venue_id="STORE-METRO-ATLANTIC-01"):
        if not isinstance(venue_id, str) or not venue_id.strip():
            raise ValueError("venue_id must be a non-empty string.")
        self.venue_id = venue_id
        self.campaign_registry = dict(CAMPAIGN_REGISTRY)

    def dispatch_campaign(self, campaign_mode, ambient_temp_c):
        if campaign_mode not in self.campaign_registry:
            raise ValueError(f"Unknown commercial campaign mode: {campaign_mode}")
        temperature = _finite_real("ambient_temp_c", ambient_temp_c)
        profile = self.campaign_registry[campaign_mode]
        power_draw = 45.0 + profile["target_rpm"] * 0.02
        thermal_safe = temperature <= 38.0 and profile["target_rpm"] <= 800
        return {
            "venue_id": self.venue_id,
            "active_campaign": campaign_mode,
            "target_asset": profile["asset"],
            "synthetic_fan_target_rpm": profile["target_rpm"],
            "campaign_priority": profile["priority"],
            "ambient_temperature_c": temperature,
            "estimated_power_draw_watts": power_draw,
            "hardware_safety_status": (
                "SYNTHETIC_THERMAL_CHECK_PASS" if thermal_safe
                else "SYNTHETIC_THERMAL_WARNING"
            ),
            "hardware_command_issued": False,
            "customer_identity_collected": False,
            "epistemic_label": "BOUNDED_SYNTHETIC_CAMPAIGN_DISPATCH",
        }


class ElevenDimensionalObserver:
    spatial_dims = 9
    observer_dims = 2

    def calibrate_axes(self, raw_telemetry, human_empathy_intent_score):
        telemetry = [_finite_real("raw telemetry", value) for value in raw_telemetry]
        if len(telemetry) != self.spatial_dims:
            raise ValueError("raw_telemetry must contain exactly 9 values.")
        empathy = _finite_real("human_empathy_intent_score", human_empathy_intent_score)
        if not 0.0 <= empathy <= 1.0:
            raise ValueError("Empathy proxy must be normalized within [0, 1].")
        d10 = sum(math.sin(value) for value in telemetry) / self.spatial_dims
        magnitude = math.sqrt(sum(value ** 2 for value in telemetry) + d10 ** 2 + empathy ** 2)
        return {
            "spatial_dimensions": self.spatial_dims,
            "observer_dimensions": self.observer_dims,
            "d10_self_knowing_factor": d10,
            "d11_empathetic_alignment_proxy": empathy,
            "d11_empathetic_alignment": empathy,
            "eleven_d_magnitude": magnitude,
            "social_proxy_status": (
                "ALIGNMENT_PROXY_PASS" if empathy >= 0.70
                else "ALIGNMENT_PROXY_RECALIBRATION_REQUIRED"
            ),
            "social_philosophy_status": (
                "ALIGNED_FOR_HUMAN_GOOD" if empathy >= 0.75
                else "RECALIBRATION_REQUIRED"
            ),
        }


def _success_criteria(results):
    dispatch = results["commercial_dispatcher"]
    observer = results["eleven_dimensional_calibration"]
    criteria = {
        "license_verification_pass": results["commercial_license_status"].endswith("VERIFIED"),
        "campaign_profile_resolved": bool(dispatch["target_asset"]),
        "synthetic_thermal_check_pass": dispatch["hardware_safety_status"] == "SYNTHETIC_THERMAL_CHECK_PASS",
        "no_hardware_command_issued": dispatch["hardware_command_issued"] is False,
        "no_customer_identity_collected": dispatch["customer_identity_collected"] is False,
        "nine_plus_two_dimensions_present": (
            observer["spatial_dimensions"] == 9
            and observer["observer_dimensions"] == 2
        ),
        "educational_alignment_proxy_pass": observer["d11_empathetic_alignment_proxy"] >= 0.70,
    }
    return {
        "criteria": criteria,
        "overall_success": all(criteria.values()),
        "interpretation": (
            "All synthetic HoloPulse research gates passed"
            if all(criteria.values())
            else "One or more synthetic HoloPulse gates failed"
        ),
    }


def execute_holopulse_simulation(
    seed=42,
    mode="BLACK_FRIDAY_FLASH",
    license_token=None,
    authorized_token_sha256=None,
):
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer.")
    protector = CommercialLicenseProtector(license_token, authorized_token_sha256)
    if not protector.verify_license():
        raise PermissionError("License token digest verification failed.")
    local_rng = random.Random(seed)
    dispatcher = HoloPulseCommercialDispatcher()
    observer = ElevenDimensionalObserver()
    telemetry_9d = [local_rng.uniform(0.2, 0.9) for _ in range(9)]
    results = {
        "commercial_dispatcher": dispatcher.dispatch_campaign(mode, ambient_temp_c=24.5),
        "eleven_dimensional_calibration": observer.calibrate_axes(
            telemetry_9d, human_empathy_intent_score=0.92
        ),
        "commercial_license_status": protector.status(),
    }
    results["success_criteria"] = _success_criteria(results)
    payload = {
        "metadata": {
            "engine": "holopulse_commercial_engine.py",
            "version": VERSION,
            "seed": seed,
            "framework": "HoloPulse Commercial Dispatch Research Diagnostic",
            "epistemic_status": "synthetic_research_model",
            "license_scope": "AGPL-3.0-only research core; external commercial authorization required",
            "determinism": "runtime timestamp excluded; local RNG used",
        },
        "simulation_results": results,
    }
    payload["provenance_sha256"] = _hash(payload)
    return payload


def main():
    parser = argparse.ArgumentParser(description="HoloPulse Commercial Dispatch Research Diagnostic")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed")
    parser.add_argument("--mode", choices=sorted(CAMPAIGN_REGISTRY), default="BLACK_FRIDAY_FLASH")
    parser.add_argument("--license", dest="license_token", default=None, help="Token to verify")
    parser.add_argument("--license-sha256", dest="authorized_token_sha256", default=None, help="External expected token digest")
    parser.add_argument("--output", default="holopulse_audit.json", help="Output report path")
    args = parser.parse_args()
    try:
        report = execute_holopulse_simulation(
            seed=args.seed,
            mode=args.mode,
            license_token=args.license_token,
            authorized_token_sha256=args.authorized_token_sha256,
        )
        with open(args.output, "w", encoding="utf-8") as output_file:
            json.dump(report, output_file, indent=2, ensure_ascii=False)
            output_file.write("\n")
        print(f"[SUCCESS] HoloPulse research diagnostic completed for [{args.mode}].")
        print(f"Cryptographic Provenance SHA-256: {report['provenance_sha256']}")
        print(f"Report saved to: {args.output}")
        print(json.dumps(report["simulation_results"], indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError, PermissionError) as error:
        print(f"[ERROR] HoloPulse diagnostic failed: {error}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
