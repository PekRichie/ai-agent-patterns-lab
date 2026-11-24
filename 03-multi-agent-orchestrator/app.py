"""Többágenses munkafolyamat-koordinátor (Planner -> Builder -> Reviewer)."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class TaskContext:
    goal: str
    plan: list[str] = field(default_factory=list)
    artifact: str = ""
    review_notes: list[str] = field(default_factory=list)
    approved: bool = False
    rounds: int = 0


class MultiAgentOrchestrator:
    def __init__(
        self,
        planner: Callable[[str], list[str]],
        builder: Callable[[TaskContext], str],
        reviewer: Callable[[TaskContext], tuple[bool, str]],
        max_rounds: int = 3,
    ) -> None:
        self.planner = planner
        self.builder = builder
        self.reviewer = reviewer
        self.max_rounds = max_rounds

    def execute(self, goal: str) -> TaskContext:
        ctx = TaskContext(goal=goal, plan=self.planner(goal))
        for r in range(1, self.max_rounds + 1):
            ctx.rounds = r
            ctx.artifact = self.builder(ctx)
            ok, note = self.reviewer(ctx)
            ctx.review_notes.append(note)
            if ok:
                ctx.approved = True
                break
        return ctx
