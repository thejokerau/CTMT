## Release & Branch Strategy (Best Practice)

Use separate long-lived branches for release channels:

- **`main`** → stable production-ready channel
- **`nightly`** → fast-moving integration channel for newest changes

Recommended workflow:

1. Develop features on short-lived feature branches.
2. Merge feature branches into `nightly` first.
3. Promote tested changes from `nightly` into `main` on cadence.

## Script Layout

To mirror the channels in the repo structure:

- **Stable script:** `stable/BTC3.py`
- **Nightly script:** `nightly/BTC-beta.py`

## Requirements

Install dependencies:

```bash
pip install pandas numpy plotly yfinance requests pandas_ta optuna
```

Python:

- Nightly script targets **Python 3.13+** and is primarily tested on **3.13.x**.

Optional acceleration dependency:

```bash
pip install cupy-cuda12x
```

If CuPy/CUDA is not available, nightly falls back to CPU automatically.

## Running

Stable channel (`main` branch target):

```bash
python stable/BTC3.py
```

Nightly channel (`nightly` branch target):

```bash
python nightly/BTC-beta.py
```

## Nightly Highlights (`nightly/BTC-beta.py`)

- User-selectable analysis interval: `1d`, `4h`, `8h`, `12h`
- Backtest lookback selector: `1/3/6/12/18/24 months`
- Accurate period math using `365.25` days/year
- Dynamic Fibonacci swing detection with support/resistance guards
- ATR/ADX/OBV/CMF risk-scoring integration
- Live setup analytics and reliability scoring:
  - regime tagging (`Trending`, `Choppy`, `High-Vol`, `Transitional`)
  - setup expectancy/win-rate/false-signal estimates
  - risk-cone and post-entry drawdown context
- Portfolio-aware live context:
  - concentration warning based on rolling correlations
  - lower-correlation alternatives to top-ranked asset
- Walk-forward auto-tuning with Optuna
- Hard risk constraints in tuning:
  - validation fold drawdown constraint (trials are pruned when exceeded)
  - position-size search bounded by configured max exposure
  - safe fallback when all trials are pruned (uses base config)
- Optional post-tune constrained retry in backtest mode:
  - if final-window drawdown exceeds target, a tighter exposure re-tune pass is attempted
- CPU parallelism:
  - Indicator cache build worker selection
  - Optuna trial parallel jobs
- CUDA detection via CuPy with safe CPU fallback
- Binance symbol pre-filtering using `exchangeInfo` to reduce bad ticker noise
- Backtest churn controls:
  - `min_hold_bars` before signal exits
  - `cooldown_bars` after exits
  - same-asset re-entry cooldown bars
  - max consecutive same-asset entries
- Action-label UI fallback:
  - auto-detects terminal support for emoji and ANSI color
  - falls back to plain text labels if unsupported
  - optional env override: `CTMT_DISABLE_EMOJI=1`
  - optional color controls: `NO_COLOR=1` or `FORCE_COLOR=1`

## Notes

On first run, the scripts will create/use `crypto_data.db` and populate market data.
Subsequent runs are faster due to caching.

## Automated Research Loop

You can now run unattended experiment cycles that:

1. Execute scheduled backtests + Optuna studies across `experiments/scenarios.json`
2. Log artifacts into `experiments/runs/` and `experiments/candidates.jsonl`
3. Promote winners into `experiments/registry/champions.json` using risk gates
4. Refresh the automation section in `PROJECT_HANDOFF.md`

Commands:

```bash
python scripts/run_experiments.py --enable-optuna
python scripts/promote_champion.py
python scripts/update_handoff.py
```

One-shot orchestrator:

```bash
python scripts/auto_research_cycle.py
```

Windows Task Scheduler helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\register_research_task.ps1 -TaskName CTMT_Nightly_Research -Time 02:00 -PythonExe python
```

Promotion gates (`scripts/promote_champion.py`) are conservative by default:

- minimum return improvement: `+1.0%`
- maximum drawdown increase allowed vs champion: `+1.5%`
- maximum sharpe drop allowed vs champion: `-0.10`

Detailed automation reference: `docs/AUTOMATION.md`
