from __future__ import annotations
from typing import Dict, List

BR_COV: Dict[str, List[bool]] = {}

def cov_init(func: str, slots: int = 100) -> None:
    global BR_COV
    BR_COV = {}
    BR_COV["get_base_ocel"] = {i: False for i in range(30)}

def cov_hit(func: str, branch_id: int) -> None:

    BR_COV[func][branch_id] = True

def cov_report() -> str:
    lines: list[str] = []
    for func, flags in sorted(BR_COV.items()):
        hit_ids = [i for i, f in enumerate(flags) if f]
        lines.append(f"{func}: {len(hit_ids)}/{len(flags)} branches hit")
        lines.append(f"  hit IDs: {hit_ids}")
    return "\n".join(lines)
