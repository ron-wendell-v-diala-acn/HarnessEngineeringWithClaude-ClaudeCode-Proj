"""Layer 3 fork: copy hot state into an isolated working directory per hypothesis.

`fork_session` here is the application-side framing: the SDK / CLI primitive lives at
Layer 2; here we reproduce the *semantics* (shared baseline, isolated scratchpads,
no cross-contamination) using state-file copies.
"""

from __future__ import annotations

import shutil
from collections.abc import Iterable
from pathlib import Path

from .scratchpad import Scratchpad


def fork_for_hypothesis(
    base_hot_state_path: Path,
    hypothesis_id: str,
    forks_root: Path,
) -> Path:
    """Create a per-hypothesis working directory and copy the base hot state into it.

    The base file's bytes remain untouched (shared baseline, read-only in practice).
    Returns the fork directory path.
    """
    fork_dir = forks_root / hypothesis_id
    fork_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(base_hot_state_path, fork_dir / "hot_state.json")
    return fork_dir


def merge_findings(scratchpad_paths: Iterable[Path], main_scratchpad: Path) -> None:
    """Append every entry from each fork's scratchpad into the main scratchpad.

    Routes every appended entry through Scratchpad.append() to preserve fsync
    durability semantics. Skips fork paths that don't exist.
    """
    main = Scratchpad(main_scratchpad)
    for path in scratchpad_paths:
        if not path.exists():
            continue
        fork_scratchpad = Scratchpad(path)
        for entry in fork_scratchpad.read():
            main.append(entry)
