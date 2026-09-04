from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Persona(str, Enum):
    DEVELOPER = "developer"
    AI_STUDENT = "ai_student"
    GAMER = "gamer"
    MARKETER = "marketer"
    CASUAL = "casual"


@dataclass
class Post:
    post_id: int
    text: str
    likes: int = 0
    comments: List[str] = field(default_factory=list)
    shares: int = 0


@dataclass
class Bot:
    bot_id: int
    persona: Persona
    activity: float
    like_probability: float
    comment_probability: float
    share_probability: float
    active: bool = True


@dataclass
class ActionResult:
    bot_id: int
    action: str
    success: bool
    detail: str = ""
