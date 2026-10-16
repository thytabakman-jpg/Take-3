#!/usr/bin/env python3
"""Validate the Take-3 experimental kernel without optimization-dependent guards."""
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
k = yaml.safe_load((root / "KERNEL.yaml").read_text())


def require(condition, message):
    if not condition:
        raise ValueError(f"Take-3 kernel fitness: {message}")


require(isinstance(k, dict), "kernel must be a mapping")
require(k.get("experiment") == "take_3_clean_room", "wrong experiment")
require(k.get("loop") == ["TASK", "DISCOVER", "DECIDE", "ACT", "VERIFY", "REENTER"], "invalid loop")
require(isinstance(k.get("records"), dict) and set(k["records"]) == {"task", "finding", "action", "result"}, "invalid records")
for name, spec in k["records"].items():
    require(isinstance(spec, dict) and isinstance(spec.get("required"), list) and bool(spec["required"]), f"missing required fields for {name}")
require(isinstance(k.get("protected"), list) and "authority_does_not_follow_from_evidence" in k["protected"], "authority guard missing")
print("Take-3 kernel fitness: PASS")
