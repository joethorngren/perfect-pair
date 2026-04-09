# Repository Guidelines

## Project Structure & Module Organization
This repository is a config-driven style generator and deployer.
- `source/`: canonical inputs. Edit `references.yaml`, `config.yaml`, and `perfect-pair-base.md`.
- `scripts/`: pipeline scripts. `sync.sh` (main entrypoint), `build.py` (primary build), `deploy.sh` (target deploy), `build.sh` (legacy).
- `generated/`: build artifacts (`perfect-pair-current.md`, `rotation-state.json`). Do not edit by hand.
- `skills/` and `cursor-versions/`: reusable templates/examples and tool-specific variants.
- Root docs (`README.md`, `WORKFLOW.md`, `CLAUDE.md`) describe usage and architecture.

## Build, Test, and Development Commands
- `./scripts/sync.sh`: creates/updates `.venv`, installs deps, builds, and deploys to all targets.
- `.venv/bin/python3 scripts/build.py`: build only, no deploy.
- `./scripts/deploy.sh`: deploy previously generated output.
- `rg "{{" generated/perfect-pair-current.md`: quick check for unreplaced template placeholders (should return no matches).

## Coding Style & Naming Conventions
- Python: follow PEP 8, 4-space indentation, `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants.
- Bash: keep `set -e`, quote variable expansions, and use uppercase env/path variables (`ROOT_DIR`, `SOURCE_FILE`).
- YAML in `source/`: 2-space indentation, clear keys (`core`, `rotating_pool`, `style_settings`), and consistent field names (`name`, `type`, `usage`, `examples`).
- Prefer small, focused script changes over broad refactors.

## Testing Guidelines
There is no formal automated test suite yet; use pipeline smoke tests:
1. Run `.venv/bin/python3 scripts/build.py`.
2. Confirm output exists and is non-empty: `test -s generated/perfect-pair-current.md`.
3. Verify no unresolved placeholders with `rg`.
4. Run `./scripts/deploy.sh` and confirm target files are updated.

## Commit & Pull Request Guidelines
Current history uses short, imperative subjects (examples: `Fix ...`, `Add ...`, `Update ...`).
- Keep commit titles concise and action-first; include scope when useful.
- In PRs, include: purpose, files changed, commands run (`build.py`, `sync.sh`), and any deploy-impact notes.
- If output behavior changes, include a short before/after snippet or summary from `generated/perfect-pair-current.md`.
