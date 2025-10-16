# KaelOS Prompt Software Quickstart

The KaelOS prompt software couples the SYSTEM_PROMPT_SOFTWARE v2.3 specification with Codex runtime scaffolding. Follow the
steps below to initialize a fresh workspace, bind the runtime to repository context, and execute the initial DALE-G cycles.

## 1. Prepare a Timestamped Working Branch
1. `VER=2.3.0`
2. `DATE=$(TZ=America/Toronto date +%Y%m%d)`
3. `TIME=$(TZ=America/Toronto date +%H%M)`
4. `git switch -c codex/prompt-software/v$VER-kaelos-omega-$DATE-$TIME`

## 2. Verify Required Files
Ensure the following paths exist before booting Codex:

- `codex/system.md`
- `codex/context-index.md`
- `codex/policies.md`
- `codex/docs/architecture.md`
- `codex/docs/kaelos-quickstart.md`
- `codex/tasks/000_onboarding.md`
- `codex/tasks/010_feature_stub.md`
- `codex/sym.log`
- `codex/hpl.jsonl`
- `requirements.txt`
- `Makefile`

Populate `codex/context-index.md` with the ordered list:

```
1) codex/policies.md
2) codex/system.md
3) codex/docs/architecture.md
4) codex/docs/kaelos-quickstart.md
5) codex/tasks/000_onboarding.md
6) codex/tasks/010_feature_stub.md
```

## 3. Configure Environment and Secrets
In the Codex UI set the environment variables:

```
PYTHONPATH=/workspace/src
CODEX_CONTEXT_PATH=/workspace/codex/context-index.md
CODEX_POLICIES_PATH=/workspace/codex/policies.md
CODEX_HPL=/workspace/codex/hpl.jsonl
CODEX_SYM=/workspace/codex/sym.log
CODEX_RUNMODE=deap
TZ=UTC
```

Only add secrets if the task requires them (OPENAI_API_KEY, GITHUB_TOKEN, NOTION_TOKEN).

## 4. Project Settings
- Container: `universal`
- Caching: On
- Internet: Off (enable temporarily for whitelisted reads only)
- Setup script:

```
set -euxo pipefail
python3 -m pip install --upgrade pip
[ -f requirements.txt ] && pip install -r requirements.txt
pytest -q || true
```

> **Coverage plugin**: The repo's `pyproject.toml` enables `--cov` flags by default. Installing `pytest-cov` (bundled in `requirements.txt`) is mandatory for clean boot and expansion runs.

## 4a. Adopt Python 3.14 Free-Threading When Needed
- Provision the free-threaded interpreter (`python3.14t`) to unlock multi-core execution for DALE-G parallel phases. Follow `codex/docs/python-3.14-free-threading.md` for environment setup, migration patterns, and risk controls.
- Activate a virtual environment with `python3.14t`, install dependencies via `pip install -r requirements.txt`, and rerun the setup script to keep coverage hooks intact.
- Run `make check-gil` (prints status) or `make check-gil-free-threaded` (fails if the GIL is active) before every BOOTRUN/EXPAND. These targets call `python -m codex_framework.utils.gil_status`, ensuring the result is captured consistently in automation logs.
- Programmatic workflows can call `python - <<'PY'` / `from codex_framework.utils import assert_free_threading; assert_free_threading()` to hard fail when the interpreter is not free-threaded; pass `allow_unknown=True` during transitional migrations that rely on older builds.
- Capture the output of `make check-gil` in BOOTRUN/EXPAND artifacts. A failure from `make check-gil-free-threaded` signals that catalyst `GC-002-A` and a SYM attestation entry are required.

## 5. Boot Command (Container Shell)
```
: > codex/sym.log
: > codex/hpl.jsonl
python - <<'PY'
print("context:", open("codex/context-index.md").read().splitlines()[:4])
print("system-len:", len(open("codex/system.md").read()))
PY
make test || true
```

## 6. Issue the First Task to Codex
Paste the BOOTRUN instructions into the Codex task input:

```
BOOTRUN:
- Read files in CODEX_CONTEXT_PATH order.
- Load SYSTEM_PROMPT_SOFTWARE v2.3 from codex/system.md.
- Execute one full DALE-G cycle on Task 000 (onboarding):
  1) verify repo, run tests, and note results
  2) write at least one heuristic to codex/hpl.jsonl
  3) append SYM entries with NONCE_8 continuity
  4) propose next catalyst (GC-002-A then GC-003-A)
- Output the JSON per “OUTPUT CONTRACT” in system.md.
- Then execute Task 010 and log again.
```

## 7. Run the Self-Expansion Loop
Submit the EXPAND follow-up task:

```
EXPAND:
- Run catalysts: GC-002-A → GC-003-A → GC-004-A → GC-007 → GC-010.
- For each:
  - enforce constraint tier A→B→C with CLA proof
  - write HPL (REINFORCE or SYNTHESIZE)
  - append SYM with two-nonce continuity
- Return scores and next-catalyst.
```

## 8. Verify Repository Usage
Run the validation commands and inspect artifacts:

```
tail -n 20 codex/sym.log
wc -l codex/hpl.jsonl && tail -n 5 codex/hpl.jsonl
pytest -q || true
```

## 9. Commit and Open a Pull Request
```
git add codex system docs src Makefile requirements.txt
git commit -m "feat(codex): boot v2.3 prompt software; init HPL/SYM"
git push -u origin HEAD
```

Include the last 10 lines of `codex/sym.log`, any new HPL entries, and `make test` output in the PR description when possible.
