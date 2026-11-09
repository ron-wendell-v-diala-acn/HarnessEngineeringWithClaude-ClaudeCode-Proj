"""Tiered compression: summarize resolved segments; preserve active verbatim.

Resolved segments are condensed by a single Claude call per segment using the
prompt template at `retail_context/prompts/compression_prompt.md`. The active
segment is **never** summarized — it is preserved byte-exact.
"""
from __future__ import annotations

from dataclasses import dataclass
from importlib import resources

from retail_context.client import complete_with_system
from retail_context.transcript import Segment, Transcript


@dataclass
class Summary:
    issue_id: str
    text: str
    input_tokens: int
    output_tokens: int


@dataclass
class Compressed:
    summaries: dict[str, Summary]
    active_text: str
    active_issue_id: str


def _load_prompt() -> str:
    return resources.files("retail_context.prompts").joinpath(
        "compression_prompt.md"
    ).read_text()


def summarize_segment(segment: Segment, *, model: str | None = None) -> Summary:
    """Summarize ONE resolved segment via a single Claude call."""
    # Guard: refuse to summarize active segments
    if segment.status != "resolved":
        raise ValueError(
            f"Cannot compress segment with status '{segment.status}' (issue_id='{segment.issue_id}'). "
            "Only resolved segments are compressed — the active segment must be preserved byte-exact."
        )
    
    # Load the compression prompt template
    system = _load_prompt()
    
    # Build the user message
    user = (
        f"Source segment — issue_id `{segment.issue_id}`, turns "
        f"{segment.turn_range[0]}-{segment.turn_range[1]}:\n\n{segment.text}"
    )
    
    # Call Claude
    text, input_tokens, output_tokens = complete_with_system(
        system, user, model=model, max_tokens=1024
    )
    
    # Return a Summary
    return Summary(
        issue_id=segment.issue_id,
        text=text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )


def compress(transcript: Transcript, *, model: str | None = None) -> Compressed:
    """Orchestrate compression across all segments."""
    summaries: dict[str, Summary] = {}
    active_text: str | None = None
    active_issue_id: str | None = None
    
    for segment in transcript.segments:
        if segment.status == "resolved":
            # Summarize resolved segments
            summary = summarize_segment(segment, model=model)
            summaries[segment.issue_id] = summary
        elif segment.status == "active":
            # Preserve active segment byte-exact
            active_text = "\n\n".join(t.render() for t in segment.turns)
            active_issue_id = segment.issue_id
    
    # Ensure we have exactly one active segment
    if active_text is None or active_issue_id is None:
        raise RuntimeError(
            "No active segment found in transcript. "
            "The assembled context requires exactly one active segment at the bottom boundary."
        )
    
    return Compressed(
        summaries=summaries,
        active_text=active_text,
        active_issue_id=active_issue_id,
    )
