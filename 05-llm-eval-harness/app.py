"""Automatikus LLM Prompt-értékelő (Eval Harness) regressziós teszteléshez."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class EvalCase:
    case_id: str
    prompt: str
    must_contain: list[str] = field(default_factory=list)
    must_not_contain: list[str] = field(default_factory=list)
    max_chars: int = 2000


def run_eval(cases: list[EvalCase], model_fn: Callable[[str], str]) -> dict[str, object]:
    results = []
    passed = 0
    for c in cases:
        out = model_fn(c.prompt)
        low = out.lower()
        ok_req = all(k.lower() in low for k in c.must_contain)
        ok_forb = all(k.lower() not in low for k in c.must_not_contain)
        ok_len = len(out) <= c.max_chars
        ok = ok_req and ok_forb and ok_len
        if ok:
            passed += 1
        results.append({"case_id": c.case_id, "passed": ok, "length": len(out)})
    score = round((passed / max(1, len(cases))) * 100.0, 1)
    return {"passed": passed, "total": len(cases), "score_pct": score, "results": results}
