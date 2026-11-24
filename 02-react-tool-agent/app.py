"""ReAct (Reason + Act) tool-calling ügynök-hurok lépéskorláttal és nyomkövetéssel."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class AgentStep:
    step: int
    thought: str
    tool: str | None = None
    tool_input: dict | None = None
    observation: str = ""


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Callable[[dict], str]] = {}

    def register(self, name: str, fn: Callable[[dict], str]) -> None:
        self._tools[name] = fn

    def call(self, name: str, args: dict) -> str:
        if name not in self._tools:
            return f"ERROR: ismeretlen eszköz ({name})"
        return self._tools[name](args)


class ReActAgent:
    def __init__(self, registry: ToolRegistry, planner: Callable[[str, list[AgentStep]], dict], max_steps: int = 5) -> None:
        self.registry = registry
        self.planner = planner
        self.max_steps = max_steps

    def run(self, goal: str) -> dict[str, object]:
        trace: list[AgentStep] = []
        for step_num in range(1, self.max_steps + 1):
            decision = self.planner(goal, trace)
            if decision.get("final_answer") is not None:
                trace.append(AgentStep(step=step_num, thought=decision.get("thought", "Kész")))
                return {"answer": decision["final_answer"], "steps": len(trace), "trace": trace}
            tool = decision["tool"]
            args = decision.get("args", {})
            obs = self.registry.call(tool, args)
            trace.append(AgentStep(step=step_num, thought=decision.get("thought", ""), tool=tool, tool_input=args, observation=obs))
        return {"answer": "Lépéskorlát elérve.", "steps": len(trace), "trace": trace}
