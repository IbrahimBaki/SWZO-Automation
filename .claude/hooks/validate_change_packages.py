#!/usr/bin/env python3
"""Validate changes/<id>/ packages: manifest schema, required files per
lifecycle state, update-set.xml well-formedness, and approval evidence
before a package can be marked committed.

Exit 0 = all good. Exit 1 = problems found (printed to stderr).
Does not touch ServiceNow or the network. Local file checks only.
"""
import sys
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHANGES_DIR = ROOT / "changes"

LIFECYCLE_STATES = [
    "draft", "planned", "xml-generated", "peer-reviewed", "imported",
    "previewed", "awaiting-human-approval", "committed", "verified",
    "rolled-back",
]

# Minimum index at which a given file must exist.
REQUIRES_PLAN_FROM = LIFECYCLE_STATES.index("planned")
REQUIRES_XML_FROM = LIFECYCLE_STATES.index("xml-generated")
REQUIRES_VERIFICATION_FROM = LIFECYCLE_STATES.index("imported")
REQUIRES_EVIDENCE_FROM = LIFECYCLE_STATES.index("previewed")

REQUIRED_MANIFEST_KEYS = [
    "change_id", "title", "pdi_target", "source_baseline",
    "affected_components", "xml_artifact", "lifecycle_state",
]


def load_manifest(path):
    """Parse manifest.yaml with PyYAML if available, else a minimal
    top-level key:value line scanner (handles this project's flat schema
    well enough to validate without requiring PyYAML on every machine)."""
    text = path.read_text()
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        data = {}
        for line in text.splitlines():
            line = line.split("#", 1)[0].rstrip()
            if not line or line.startswith((" ", "\t", "-")):
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = value
        return data


def check_package(pkg_dir, errors):
    name = pkg_dir.name
    manifest_path = pkg_dir / "manifest.yaml"
    if not manifest_path.exists():
        errors.append(f"{name}: missing manifest.yaml")
        return

    try:
        manifest = load_manifest(manifest_path)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{name}: manifest.yaml failed to parse ({exc})")
        return

    for key in REQUIRED_MANIFEST_KEYS:
        if key not in manifest or manifest[key] in (None, ""):
            errors.append(f"{name}: manifest.yaml missing required key '{key}'")

    state = manifest.get("lifecycle_state")
    if state not in LIFECYCLE_STATES:
        errors.append(
            f"{name}: lifecycle_state '{state}' is not one of {LIFECYCLE_STATES}"
        )
        return
    state_idx = LIFECYCLE_STATES.index(state)

    if state_idx >= REQUIRES_PLAN_FROM and not (pkg_dir / "plan.md").exists():
        errors.append(f"{name}: lifecycle_state is '{state}' but plan.md is missing")

    xml_path = pkg_dir / "update-set.xml"
    if state_idx >= REQUIRES_XML_FROM and not xml_path.exists():
        errors.append(
            f"{name}: lifecycle_state is '{state}' but update-set.xml is missing"
        )
    if xml_path.exists():
        try:
            ET.parse(xml_path)
        except ET.ParseError as exc:
            errors.append(f"{name}: update-set.xml is not well-formed XML ({exc})")
        if manifest.get("xml_artifact") == "pending":
            errors.append(
                f"{name}: update-set.xml exists on disk but manifest.yaml still says "
                f"xml_artifact: pending"
            )
    elif manifest.get("xml_artifact") not in (None, "pending"):
        errors.append(
            f"{name}: manifest.yaml points xml_artifact at a file that doesn't exist"
        )

    verification_path = pkg_dir / "verification.md"
    if state_idx >= REQUIRES_VERIFICATION_FROM and not verification_path.exists():
        errors.append(
            f"{name}: lifecycle_state is '{state}' but verification.md is missing"
        )

    evidence_dir = pkg_dir / "evidence"
    if state_idx >= REQUIRES_EVIDENCE_FROM:
        has_evidence = evidence_dir.is_dir() and any(
            p.name != ".gitkeep" for p in evidence_dir.iterdir()
        )
        if not has_evidence:
            errors.append(
                f"{name}: lifecycle_state is '{state}' but evidence/ has no captured evidence"
            )

    if state == "committed":
        if not verification_path.exists():
            errors.append(f"{name}: cannot be 'committed' without verification.md")
        else:
            vtext = verification_path.read_text()
            section = vtext.split("## Human approval", 1)
            approval_block = section[1].split("##", 1)[0] if len(section) > 1 else ""
            approved_by_line = next(
                (l for l in approval_block.splitlines() if l.strip().startswith("- Approved by:")),
                "",
            )
            value = approved_by_line.split(":", 1)[1].strip() if ":" in approved_by_line else ""
            if not value or value.startswith("<"):
                errors.append(
                    f"{name}: lifecycle_state is 'committed' but verification.md has no "
                    f"'Approved by' value under '## Human approval' — commit requires recorded "
                    f"human approval evidence for this exact package"
                )


def main():
    if not CHANGES_DIR.is_dir():
        print("No changes/ directory found — nothing to validate.")
        return 0

    errors = []
    for pkg_dir in sorted(CHANGES_DIR.iterdir()):
        if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
            continue
        check_package(pkg_dir, errors)

    if errors:
        print("Change package validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("Change package validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
