from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List

from .models import ActionResult


@dataclass
class DetectionReport:
    total_actions: int
    successful_actions: int
    unique_bots: int
    repeated_comment_ratio: float
    burst_score: float
    suspicion_score: float
    label: str


class BotDetector:
    """Simple heuristic detector for the simulator's generated activity."""

    def analyze(self, results: Iterable[ActionResult]) -> DetectionReport:
        rows: List[ActionResult] = list(results)
        successful = [row for row in rows if row.success]
        unique_bots = len({row.bot_id for row in successful})

        comments = [
            row.detail
            for row in successful
            if row.action == "comment" and row.detail
        ]

        repeated_comment_ratio = 0.0
        if comments:
            counts = Counter(comments)
            duplicates = sum(max(0, count - 1) for count in counts.values())
            repeated_comment_ratio = duplicates / len(comments)

        burst_score = min(1.0, len(successful) / 1000.0)

        diversity_penalty = repeated_comment_ratio
        concentration = 0.0
        if successful:
            concentration = min(1.0, len(successful) / max(unique_bots, 1) - 1.0)

        suspicion = min(
            1.0,
            0.60 * burst_score
            + 0.30 * diversity_penalty
            + 0.10 * concentration,
        )

        if suspicion >= 0.70:
            label = "high"
        elif suspicion >= 0.40:
            label = "medium"
        else:
            label = "low"

        return DetectionReport(
            total_actions=len(rows),
            successful_actions=len(successful),
            unique_bots=unique_bots,
            repeated_comment_ratio=round(repeated_comment_ratio, 3),
            burst_score=round(burst_score, 3),
            suspicion_score=round(suspicion, 3),
            label=label,
        )
