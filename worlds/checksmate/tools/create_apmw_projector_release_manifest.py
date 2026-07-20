"""Create an immutable ChecksMate release manifest from frozen projector archives."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile
from typing import Any, Sequence


BUILD_MANIFEST_SCHEMA = "apmw_projector_build_manifest"
BUILD_MANIFEST_VERSION = 1
RELEASE_MANIFEST_SCHEMA = "apmw_projector_release_manifest"
RELEASE_MANIFEST_VERSION = 1
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_RELEASE_TAG = re.compile(r"^apmw-projector-v[0-9A-Za-z.+-]+$")
_SEMANTIC_VERSION = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)
_PLATFORMS = {"windows", "linux", "macos"}
_ARCHITECTURES = {"x86", "x64", "arm64"}
_REQUIRED_ASSET_IDS = {"windows-x86", "windows-x64"}


@dataclass(frozen=True)
class ReleaseInput:
    build_manifest: Path
    archive: Path


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def create_release_manifest(
    inputs: Sequence[ReleaseInput],
    source_repository: str,
    source_commit: str,
    release_tag: str,
) -> dict[str, Any]:
    _validate_release_identity(source_repository, source_commit, release_tag)
    if len(inputs) != 2:
        raise ValueError("exactly two projector build inputs are required")

    seen_files: set[Path] = set()
    metadata: dict[str, Any] | None = None
    assets: dict[str, dict[str, Any]] = {}
    for item in inputs:
        manifest_path = _input_file(item.build_manifest, seen_files, "build manifest")
        archive_path = _input_file(item.archive, seen_files, "archive")
        if archive_path.suffix.lower() != ".zip" or not zipfile.is_zipfile(archive_path):
            raise ValueError(f"archive is not a zip file: {archive_path}")

        build_manifest, manifest_bytes = _read_build_manifest(manifest_path)
        _verify_archive(archive_path, build_manifest, manifest_bytes)
        current_metadata = {
            key: build_manifest[key]
            for key in (
                "runtime_semantic_version",
                "protocol_version",
                "contract_hash",
            )
        }
        if metadata is None:
            metadata = current_metadata
        elif metadata != current_metadata:
            raise ValueError("build manifests have mismatched projector metadata")

        asset_id = (
            f"{build_manifest['target_platform']}-"
            f"{build_manifest['target_architecture']}"
        )
        if asset_id in assets:
            raise ValueError(f"duplicate projector architecture: {asset_id}")
        assets[asset_id] = {
            "filename": archive_path.name,
            "sha256": sha256_file(archive_path),
            "size": archive_path.stat().st_size,
            "executable": {
                "relative_path": build_manifest["executable_relative_path"],
                "sha256": build_manifest["executable_sha256"],
            },
        }

    assert metadata is not None
    if set(assets) != _REQUIRED_ASSET_IDS:
        raise ValueError(
            "release must contain exactly windows-x86 and windows-x64 projector assets"
        )
    expected_tag = f"apmw-projector-v{metadata['runtime_semantic_version']}"
    if release_tag != expected_tag:
        raise ValueError(
            f"release tag must equal the projector runtime version: {expected_tag}"
        )
    return {
        "schema": RELEASE_MANIFEST_SCHEMA,
        "version": RELEASE_MANIFEST_VERSION,
        **metadata,
        "source_repository": source_repository,
        "source_commit": source_commit,
        "release_tag": release_tag,
        "assets": assets,
    }


def write_release_manifest(manifest: dict[str, Any], output: Path) -> Path:
    output = output.resolve()
    if output.exists():
        raise ValueError(f"release manifest already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(canonical_json(manifest) + "\n", encoding="ascii")
    return output


def _validate_release_identity(
    source_repository: str, source_commit: str, release_tag: str
) -> None:
    if not _REPOSITORY.fullmatch(source_repository):
        raise ValueError("source repository must be an owner/repository identifier")
    if not _COMMIT.fullmatch(source_commit):
        raise ValueError("source commit must be a lowercase 40-hex identifier")
    if not _RELEASE_TAG.fullmatch(release_tag):
        raise ValueError("release tag must be an apmw-projector-v tag")


def _input_file(path: Path, seen: set[Path], kind: str) -> Path:
    resolved = path.resolve()
    if resolved in seen:
        raise ValueError(f"duplicate input file: {resolved}")
    if not resolved.is_file():
        raise ValueError(f"{kind} is not a regular file: {resolved}")
    seen.add(resolved)
    return resolved


def _read_build_manifest(path: Path) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        document = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=_reject_duplicate_properties,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"build manifest is not valid ASCII JSON: {path}") from error
    required = {
        "schema",
        "version",
        "runtime_semantic_version",
        "protocol_version",
        "contract_hash",
        "target_platform",
        "target_architecture",
        "executable_relative_path",
        "executable_sha256",
    }
    if not isinstance(document, dict) or set(document) != required:
        raise ValueError(f"build manifest has invalid fields: {path}")
    if (
        not isinstance(document["schema"], str)
        or document["schema"] != BUILD_MANIFEST_SCHEMA
        or not isinstance(document["version"], int)
        or isinstance(document["version"], bool)
        or document["version"] != BUILD_MANIFEST_VERSION
    ):
        raise ValueError(f"build manifest has unsupported schema/version: {path}")
    if (
        not isinstance(document["runtime_semantic_version"], str)
        or not _SEMANTIC_VERSION.fullmatch(document["runtime_semantic_version"])
        or not isinstance(document["protocol_version"], int)
        or isinstance(document["protocol_version"], bool)
        or document["protocol_version"] < 1
        or not isinstance(document["contract_hash"], str)
        or not _SHA256.fullmatch(document["contract_hash"])
        or not isinstance(document["target_platform"], str)
        or document["target_platform"] not in _PLATFORMS
        or not isinstance(document["target_architecture"], str)
        or document["target_architecture"] not in _ARCHITECTURES
        or not _safe_relative_path(document["executable_relative_path"])
        or not isinstance(document["executable_sha256"], str)
        or not _SHA256.fullmatch(document["executable_sha256"])
    ):
        raise ValueError(f"build manifest has invalid metadata: {path}")
    return document, raw


def _reject_duplicate_properties(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    document = {}
    for key, value in pairs:
        if key in document:
            raise ValueError(f"duplicate JSON property: {key}")
        document[key] = value
    return document


def _verify_archive(
    archive_path: Path, build_manifest: dict[str, Any], manifest_bytes: bytes
) -> None:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            members = _validated_members(archive, archive_path)
            embedded_manifest = _required_member(
                archive, members, "apmw-projector-manifest.json", archive_path
            )
            embedded_bytes = archive.read(embedded_manifest)
            if embedded_bytes != manifest_bytes:
                raise ValueError(
                    f"archive manifest does not match supplied build manifest: {archive_path}"
                )
            try:
                embedded_document = json.loads(
                    embedded_bytes.decode("ascii"),
                    object_pairs_hook=_reject_duplicate_properties,
                )
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValueError(
                    f"archive contains an invalid embedded build manifest: {archive_path}"
                ) from error
            if embedded_document != build_manifest:
                raise ValueError(
                    f"archive manifest content does not match supplied build manifest: {archive_path}"
                )

            executable = _required_member(
                archive,
                members,
                build_manifest["executable_relative_path"],
                archive_path,
            )
            if sha256_bytes(archive.read(executable)) != build_manifest["executable_sha256"]:
                raise ValueError(
                    f"archive executable hash does not match build manifest: {archive_path}"
                )
    except zipfile.BadZipFile as error:
        raise ValueError(f"archive is not a readable zip file: {archive_path}") from error


def _validated_members(
    archive: zipfile.ZipFile, archive_path: Path
) -> dict[str, zipfile.ZipInfo]:
    members = {}
    casefolded = set()
    for member in archive.infolist():
        path = _safe_zip_member_path(member.filename, archive_path)
        if path in members or path.casefold() in casefolded:
            raise ValueError(f"archive contains duplicate member path: {archive_path}")
        if (
            stat.S_ISLNK((member.external_attr >> 16) & 0o170000)
            or member.external_attr & 0x400
        ):
            raise ValueError(f"archive contains link-like member: {archive_path}")
        members[path] = member
        casefolded.add(path.casefold())
    return members


def _safe_zip_member_path(value: str, archive_path: Path) -> str:
    if not value or "\\" in value:
        raise ValueError(f"archive contains unsafe member path: {archive_path}")
    path = PurePosixPath(value)
    candidate = value[:-1] if value.endswith("/") else value
    segments = candidate.split("/")
    if (
        not candidate
        or path.is_absolute()
        or any(not segment or segment in {".", ".."} for segment in segments)
    ):
        raise ValueError(f"archive contains unsafe member path: {archive_path}")
    return value


def _required_member(
    archive: zipfile.ZipFile,
    members: dict[str, zipfile.ZipInfo],
    path: str,
    archive_path: Path,
) -> zipfile.ZipInfo:
    _safe_zip_member_path(path, archive_path)
    try:
        member = members[path]
    except KeyError as error:
        raise ValueError(f"archive is missing required member {path}: {archive_path}") from error
    if member.is_dir():
        raise ValueError(f"archive required member is a directory: {archive_path}")
    return member


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and all(segment and segment not in {".", ".."} for segment in value.split("/"))
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        action="append",
        nargs=2,
        metavar=("BUILD_MANIFEST", "ARCHIVE"),
        required=True,
    )
    parser.add_argument("--source-repository", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args(argv)
    try:
        manifest = create_release_manifest(
            [
                ReleaseInput(Path(manifest), Path(archive))
                for manifest, archive in arguments.input
            ],
            arguments.source_repository,
            arguments.source_commit,
            arguments.release_tag,
        )
        output = write_release_manifest(manifest, arguments.output)
    except ValueError as error:
        parser.error(str(error))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
