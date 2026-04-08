import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "PROJECT_HANDOFF.md"
RUNS_DIR = ROOT / "experiments" / "runs"
CHAMPIONS = ROOT / "experiments" / "registry" / "champions.json"

START = "<!-- AUTO_HANDBACK_START -->"
END = "<!-- AUTO_HANDBACK_END -->"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def latest_run_file() -> Optional[Path]:
    files = sorted(RUNS_DIR.glob("run_*.json"))
    return files[-1] if files else None


def scenario_summary(latest: List[Dict[str, Any]]) -> List[str]:
    lines: List[str] = []
    for rec in latest:
        sc = rec.get("scenario", {})
        sid = str(sc.get("id", "scenario"))
        sel = rec.get("selected", {})
        rs = (sel.get("result", {}) or {})
        m = (rs.get("metrics", {}) or {})
        lines.append(
            f"- `{sid}`: selected `{sel.get('name', 'n/a')}`, "
            f"return {float(rs.get('return_pct', 0.0)):+.2f}%, "
            f"maxDD {float(m.get('max_drawdown_pct', 0.0)):.2f}%, "
            f"sharpe {float(m.get('sharpe', 0.0)):.2f}"
        )
    return lines


def build_block() -> str:
    run_file = latest_run_file()
    has_run = (run_file is not None) and run_file.exists()
    run_data = read_json(run_file, []) if has_run else []
    champions = read_json(CHAMPIONS, {})
    promoted_count = len(champions) if isinstance(champions, dict) else 0

    lines: List[str] = []
    lines.append(START)
    lines.append("## Automated Research Status")
    lines.append(f"- Last update UTC: {utc_now_iso()}")
    if has_run:
        rel = run_file.relative_to(ROOT).as_posix()
        lines.append(f"- Latest experiment artifact: `{rel}`")
    else:
        lines.append("- Latest experiment artifact: none")
    lines.append(f"- Champion scenarios tracked: {promoted_count}")

    if isinstance(run_data, list) and run_data:
        lines.append("- Latest run summary:")
        lines.extend(scenario_summary(run_data))
    else:
        lines.append("- Latest run summary: no data")
    lines.append(END)
    return "\n".join(lines)


def main() -> None:
    if not HANDOFF.exists():
        raise SystemExit(f"Missing {HANDOFF}")

    content = HANDOFF.read_text(encoding="utf-8")
    block = build_block()
    if START in content and END in content:
        pre = content.split(START)[0].rstrip()
        post = content.split(END)[1].lstrip()
        updated = f"{pre}\n\n{block}\n\n{post}"
    else:
        updated = content.rstrip() + "\n\n" + block + "\n"
    HANDOFF.write_text(updated, encoding="utf-8")
    print(f"Updated handoff automation block in {HANDOFF}")


if __name__ == "__main__":
    main()
