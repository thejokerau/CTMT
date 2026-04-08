import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


def run(cmd):
    print(f"> {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT), check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main() -> None:
    run([PY, str(ROOT / "scripts" / "run_experiments.py"), "--enable-optuna"])
    run([PY, str(ROOT / "scripts" / "promote_champion.py")])
    run([PY, str(ROOT / "scripts" / "update_handoff.py")])
    print("Automated research cycle completed.")


if __name__ == "__main__":
    main()
