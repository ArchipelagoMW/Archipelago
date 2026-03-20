"""Structured logging utilities for KirbyAM generation."""

import logging
from time import perf_counter
from contextlib import contextmanager
from typing import Iterator, Optional

# Get or create logger for Kirby & The Amazing Mirror
logger = logging.getLogger("Kirby & The Amazing Mirror")


class GenerationStageLogger:
    """Context manager for logging individual generation stages."""

    def __init__(self, stage_name: str, player: int, player_name: str):
        """Initialize stage logger."""
        self.stage_name = stage_name
        self.player = player
        self.player_name = player_name
        self.start_time: Optional[float] = None

    def __enter__(self) -> "GenerationStageLogger":
        """Log stage start."""
        self.start_time = perf_counter()
        logger.info(
            f"[P{self.player}] Generation stage: {self.stage_name} (player: {self.player_name})"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Log stage completion."""
        if self.start_time is None:
            return

        elapsed = perf_counter() - self.start_time

        if exc_type is not None:
            logger.error(
                f"[P{self.player}] Generation stage '{self.stage_name}' failed after {elapsed:.2f}s: {exc_type.__name__}: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb),
            )
        else:
            logger.info(
                f"[P{self.player}] Generation stage '{self.stage_name}' completed in {elapsed:.2f}s"
            )


@contextmanager
def generation_stage(
    stage_name: str, player: int, player_name: str
) -> Iterator[GenerationStageLogger]:
    """
    Context manager to log generation stage execution.

    Usage:
        with generation_stage("create_items", self.player, self.player_name):
            # do work
            logger.debug("Item created: Shard_1")
    """
    stage_logger = GenerationStageLogger(stage_name, player, player_name)
    with stage_logger:
        yield stage_logger


def log_generation_start(player: int, player_name: str, options: dict) -> None:
    """Log the start of world generation."""
    logger.info(f"[P{player}] === KirbyAM Generation Start ===")
    logger.info(f"[P{player}] Player: {player_name}")
    logger.info(f"[P{player}] Options: goal={options.get('goal')}, shards={options.get('shards')}")


def log_generation_complete(player: int, player_name: str, elapsed: float) -> None:
    """Log successful generation completion."""
    logger.info(f"[P{player}] === KirbyAM Generation Complete for player {player_name} ===")
    logger.info(f"[P{player}] Total generation time: {elapsed:.2f}s")


def log_generation_error(player: int, player_name: str, error: str) -> None:
    """Log generation error."""
    logger.error(f"[P{player}] === KirbyAM Generation Failed for player {player_name} ===")
    logger.error(f"[P{player}] Error for player {player_name}: {error}")


def log_regions_created(player: int, region_count: int, item_count: int) -> None:
    """Log region and item creation."""
    logger.info(f"[P{player}] Created {region_count} regions with {item_count} fillable locations")


def log_items_created(player: int, item_count: int, shard_count: int, other_count: int) -> None:
    """Log item pool creation."""
    logger.info(f"[P{player}] Item pool created: {item_count} randomized items")
    logger.debug(f"[P{player}]   - Shards: {shard_count}")
    logger.debug(f"[P{player}]   - Other items: {other_count}")


def log_rules_set(player: int, rule_count: int) -> None:
    """Log rule setting."""
    logger.info(f"[P{player}] Progression rules established: {rule_count} rules defined")


def log_patch_created(player: int, patch_file: str, size: int) -> None:
    """Log patch file creation."""
    logger.info(f"[P{player}] Patch file created: {patch_file} ({size} bytes)")


def log_slot_data(player: int, slot_data: dict) -> None:
    """Log slot data."""
    logger.debug(f"[P{player}] Slot data: {slot_data}")
