#!/usr/bin/env python3
"""Build release metadata for KirbyAM APWorld tag-driven releases."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

TAG_PATTERN = re.compile(r"^kirbyam-v(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*))$")


@dataclass(frozen=True)
class ReleaseMetadata:
    apworld_name: str
    release_name: str
    release_tag: str
    version: str
    release_enabled: bool


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
            release_enabled=False,
        )

    ref_name = _tag_name_from_ref(github_ref)
    match = TAG_PATTERN.fullmatch(ref_name)
    if match:
        version = match.group("version")
        return ReleaseMetadata(
            apworld_name=f"kirbyam-{version}.apworld",
            release_name=f"KirbyAM APWorld v{version}",
            release_tag=ref_name,
            version=version,
            release_enabled=True,
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
        release_enabled=False,
    )


def write_github_output(metadata: ReleaseMetadata, output_path: Path) -> None:
    lines = [
        f"apworld_name={metadata.apworld_name}",
        f"release_name={metadata.release_name}",
        f"release_tag={metadata.release_tag}",
        f"version={metadata.version}",
        f"release_enabled={'true' if metadata.release_enabled else 'false'}",
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = build_release_metadata(args.github_ref)

    if args.github_output:
        write_github_output(metadata, Path(args.github_output))
    else:
        print(metadata)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())