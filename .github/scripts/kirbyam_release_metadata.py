#!/usr/bin/env python3
"""Build release metadata for KirbyAM APWorld tag-driven releases."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

TAG_PATTERN = re.compile(
    r"^kirbyam-v(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-rc[1-9]\d*)?)$"
)


@dataclass(frozen=True)
class ReleaseMetadata:
    apworld_name: str
    release_name: str
    release_tag: str
    version: str
    manifest_version: str
    release_enabled: bool
    prerelease: bool


def _tag_name_from_ref(github_ref: str) -> str:
    if github_ref.startswith("refs/tags/"):
        return github_ref.removeprefix("refs/tags/")
    return github_ref


def build_release_metadata(github_ref: str) -> ReleaseMetadata:
    if not github_ref.startswith("refs/tags/"):
        return ReleaseMetadata(
            apworld_name="kirbyam.apworld",
            release_name="",
            release_tag="",
            version="",
            manifest_version="",
            release_enabled=False,
            prerelease=False,
        )

    ref_name = _tag_name_from_ref(github_ref)
    match = TAG_PATTERN.fullmatch(ref_name)
    if match:
        version = match.group("version")
        manifest_version = version
        return ReleaseMetadata(
            apworld_name="kirbyam.apworld",
            release_name=f"KirbyAM APWorld v{version}",
            release_tag=ref_name,
            version=version,
            manifest_version=manifest_version,
            release_enabled=True,
            prerelease="-rc" in version,
        )

    if ref_name.startswith("kirbyam-v"):
        raise ValueError(
            "Malformed KirbyAM release tag. Expected format: kirbyam-vMAJOR.MINOR.PATCH"
        )

    return ReleaseMetadata(
        apworld_name="kirbyam.apworld",
        release_name="",
        release_tag="",
        version="",
        manifest_version="",
        release_enabled=False,
        prerelease=False,
    )


def check_changelog_has_version(changelog_path: Path, version: str) -> None:
    """Raise ValueError if the changelog does not contain a section for version.

    Looks for a heading of the exact form ``## v{version}`` anywhere in the
    file.  Raises with a descriptive message so the CI step fails clearly.
    """
    text = changelog_path.read_text(encoding="utf-8")
    heading = f"## v{version}"
    for line in text.splitlines():
        if line.strip() == heading:
            return
    raise ValueError(
        f"CHANGELOG.md does not contain a section for v{version}. "
        f"Add a '## v{version}' heading before tagging the release."
    )


def extract_changelog_section(changelog_path: Path, version: str) -> str:
    """Extract the markdown section for a single changelog version."""
    text = changelog_path.read_text(encoding="utf-8")
    heading = f"## v{version}"
    lines = text.splitlines()
    start_index = None

    for index, line in enumerate(lines):
        if line.strip() == heading:
            start_index = index
            break

    if start_index is None:
        raise ValueError(
            f"CHANGELOG.md does not contain a section for v{version}. "
            f"Add a '## v{version}' heading before tagging the release."
        )

    end_index = len(lines)
    for index in range(start_index + 1, len(lines)):
        if lines[index].startswith("## "):
            end_index = index
            break

    return "\n".join(lines[start_index:end_index]).rstrip() + "\n"


def inject_world_version(manifest_path: Path, world_version: str) -> bool:
    """Inject world_version into a world manifest JSON file.

    Returns True when a write occurred, False when no change was needed.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("world_version") == world_version:
        return False

    manifest["world_version"] = world_version
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return True


def write_github_output(metadata: ReleaseMetadata, output_path: Path) -> None:
    lines = [
        f"apworld_name={metadata.apworld_name}",
        f"release_name={metadata.release_name}",
        f"release_tag={metadata.release_tag}",
        f"version={metadata.version}",
        f"manifest_version={metadata.manifest_version}",
        f"release_enabled={'true' if metadata.release_enabled else 'false'}",
        f"prerelease={'true' if metadata.prerelease else 'false'}",
    ]
    with output_path.open("a", encoding="utf-8", newline="\n") as output_file:
        for line in lines:
            output_file.write(f"{line}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate GitHub Actions outputs for KirbyAM releases.")
    parser.add_argument("--github-ref", required=True, help="GitHub ref such as refs/tags/kirbyam-v0.0.1")
    parser.add_argument(
        "--github-output",
        default=os.environ.get("GITHUB_OUTPUT"),
        help="Path to the GitHub Actions output file.",
    )
    parser.add_argument(
        "--world-manifest",
        type=Path,
        help="Optional world manifest path to receive tag-derived world_version on release builds.",
    )
    parser.add_argument(
        "--changelog",
        type=Path,
        help="Optional path to CHANGELOG.md; on release builds, verified to contain a section for the release version.",
    )
    parser.add_argument(
        "--release-notes",
        type=Path,
        help="Optional path to write the markdown release notes extracted from CHANGELOG.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = build_release_metadata(args.github_ref)

    if args.changelog and metadata.release_enabled:
        check_changelog_has_version(args.changelog, metadata.version)
        print(f"CHANGELOG.md contains section for v{metadata.version}")

    if args.release_notes and args.changelog and metadata.release_enabled:
        args.release_notes.write_text(
            extract_changelog_section(args.changelog, metadata.version),
            encoding="utf-8",
            newline="\n",
        )

    if args.world_manifest and metadata.release_enabled:
        updated = inject_world_version(args.world_manifest, metadata.manifest_version)
        if updated:
            print(
                f"Injected world_version={metadata.manifest_version} into {args.world_manifest}",
            )
        else:
            print(
                f"world_version already set to {metadata.manifest_version} in {args.world_manifest}",
            )

    if args.github_output:
        write_github_output(metadata, Path(args.github_output))
    else:
        print(metadata)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
