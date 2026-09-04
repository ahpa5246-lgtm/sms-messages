from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Optional

from .models import ActionResult, Bot, Persona, Post


COMMENTS = {
    Persona.DEVELOPER: [
        "Interesting implementation.",
        "Would be useful to see the architecture.",
        "Nice technical demo.",
    ],
    Persona.AI_STUDENT: [
        "This is a useful AI example.",
        "I would like to test this.",
        "The agent idea is interesting.",
    ],
    Persona.GAMER: [
        "That is actually pretty cool.",
        "Nice demo.",
        "This looks fun to experiment with.",
    ],
    Persona.MARKETER: [
        "Interesting engagement pattern.",
        "The analytics would be useful here.",
        "Good demonstration of reach versus quality.",
    ],
    Persona.CASUAL: [
        "Nice post.",
        "Interesting.",
        "Cool example.",
    ],
}


@dataclass
class JobSummary:
    requested: int
    attempted: int
    completed: int
    action: str


class BotFarm:
    """A local-only simulation of an orchestrated social bot farm.

    This class never performs network requests and does not integrate with
    social-media platforms. It mutates only in-memory Post objects.
    """

    def __init__(self, bots: Iterable[Bot], seed: Optional[int] = None):
        self.bots: List[Bot] = list(bots)
        self.rng = random.Random(seed)

    @classmethod
    def generate(cls, count: int, seed: Optional[int] = None) -> "BotFarm":
        if count < 1:
            raise ValueError("count must be >= 1")

        rng = random.Random(seed)
        personas = list(Persona)
        bots = []

        for bot_id in range(1, count + 1):
            activity = rng.uniform(0.35, 1.0)
            bots.append(
                Bot(
                    bot_id=bot_id,
                    persona=rng.choice(personas),
                    activity=activity,
                    like_probability=rng.uniform(0.55, 0.98),
                    comment_probability=rng.uniform(0.03, 0.22),
                    share_probability=rng.uniform(0.01, 0.08),
                )
            )

        farm = cls(bots=bots, seed=seed)
        farm.rng = rng
        return farm

    def _eligible_bots(self) -> List[Bot]:
        bots = [bot for bot in self.bots if bot.active]
        self.rng.shuffle(bots)
        return bots

    def run_like_job(self, post: Post, target: int) -> tuple[JobSummary, List[ActionResult]]:
        if target < 0:
            raise ValueError("target must be >= 0")

        completed = 0
        results: List[ActionResult] = []

        for bot in self._eligible_bots():
            if completed >= target:
                break

            success = self.rng.random() < bot.like_probability * bot.activity
            if success:
                post.likes += 1
                completed += 1

            results.append(
                ActionResult(
                    bot_id=bot.bot_id,
                    action="like",
                    success=success,
                    detail=bot.persona.value,
                )
            )

        return (
            JobSummary(target, len(results), completed, "like"),
            results,
        )

    def run_mixed_job(self, post: Post, limit: Optional[int] = None) -> List[ActionResult]:
        results: List[ActionResult] = []
        bots = self._eligible_bots()
        if limit is not None:
            bots = bots[: max(0, limit)]

        for bot in bots:
            engagement_roll = self.rng.random()
            normalized_like = bot.like_probability * bot.activity

            if engagement_roll < normalized_like:
                post.likes += 1
                results.append(ActionResult(bot.bot_id, "like", True, bot.persona.value))

            if self.rng.random() < bot.comment_probability * bot.activity:
                comment = self.rng.choice(COMMENTS[bot.persona])
                post.comments.append(comment)
                results.append(ActionResult(bot.bot_id, "comment", True, comment))

            if self.rng.random() < bot.share_probability * bot.activity:
                post.shares += 1
                results.append(ActionResult(bot.bot_id, "share", True, bot.persona.value))

        return results
