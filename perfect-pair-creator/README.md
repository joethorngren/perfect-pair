# Perfect Pair Creator

A personalized pair programming partner for Cursor IDE, Claude Code, Gemini CLI, and Codex CLI — witty, agile-minded, and knows your cultural references.

## What This Does

Creates a custom programming partner that acts like your ideal pair, complete with:
- References to YOUR favorite shows, movies, and comedians (The Office, Parks & Rec, Arrested Development, Chappelle Show, Key & Peele, SNL, and more)
- The right balance of support vs. push-back for your style
- Playful roasting (as much or as little as you want)
- Agile-minded thinking tuned to your preferences
- A communication style that matches your vibe

## Quick Start

### 1. Clone the Repo

```bash
git clone https://github.com/joethorngren/perfect-pair.git
cd perfect-pair/perfect-pair-creator
```

### 2. Deploy to Your Tools

```bash
# Deploys to all 4 tools
./scripts/sync.sh
```

That's it! Perfect Pair is now active in:
- **Cursor** — All projects automatically (`~/.cursor/rules/perfect-pair.mdc`)
- **Claude Code** — All sessions via SessionStart hook (`~/.claude/plugins/user/perfect-pair-output-style/`)
- **Gemini CLI** — All sessions via `@import` (`~/.gemini/perfect-pair-style.md`)
- **Codex CLI** — All sessions via global instructions (`~/.codex/AGENTS.md`)

### 3. Customize

```bash
# Edit your reference library
open source/references.yaml

# Adjust personality (roast level, agile intensity, etc.)
open source/config.yaml

# Rebuild and deploy
./scripts/sync.sh
```

## Documentation

- **[WORKFLOW.md](WORKFLOW.md)** — Daily workflow guide
- **[CLAUDE.md](CLAUDE.md)** — Build system architecture (for AI assistants)
- **[CURSOR-README.md](cursor-versions/CURSOR-README.md)** — Cursor-specific details

## How It Works

### Build Pipeline

```
source/references.yaml    ──┐
source/config.yaml        ──┼──> build.py ──> generated/perfect-pair-current.md
source/perfect-pair-base.md ┘    (via .venv + PyYAML)
                                         ↓
                                   deploy.sh
                                         ↓
             ┌──────────┬──────────┬──────────┐
             ↓          ↓          ↓          ↓
      ~/.cursor/  ~/.claude/  ~/.gemini/  ~/.codex/
      rules/      plugins/   style.md    AGENTS.md
```

### Single Source of Truth

All your references live in `source/references.yaml`. Edit this file, run `./scripts/sync.sh`, done.

### Reference Library System

```yaml
core:
  # Always included - your absolute favorites
  - name: "The Office"
    usage: "Awkward code moments"
    examples: ["Michael Scott's 'that's what she said'"]

rotating_pool:
  # Rotates in/out to manage context (5 active at a time)
  - name: "Community"
    usage: "Meta discussions"
    examples: ["Cool cool cool"]
```

### Config-Driven Personality

`source/config.yaml` settings actively shape the generated output:

| Setting | Range | Effect |
|---------|-------|--------|
| `roast_level` | 1-4 | Controls roast intensity and number of examples |
| `agile_intensity` | 1-4 | Scales from practical tips to full evangelist |
| `pushback_style` | 1-4 | Ranges from trust-based to devil's advocate |
| `formality` | 1-4 | Adjusts tone from professional to best-friend casual |

### dotfiles-ai Integration

Deploy detects [GNU Stow](https://www.gnu.org/software/stow/) symlinks managed by `~/.dotfiles-ai/` and writes to the repo paths directly, keeping your dotfiles clean.

## Example Styles

We've included **5 pre-made styles** with different personalities:

1. **Original Perfect Pair** — Sharp wit, mix of comedy styles
2. **Office Comedy Fan** — Supportive, wholesome
3. **Sci-Fi Philosopher** — Logical, thoughtful
4. **British Wit** — Dry, clever
5. **Minimalist Zen** — Focused, no fluff

See all: [`cursor-versions/modern/.cursor/rules/examples/`](cursor-versions/modern/.cursor/rules/examples/)

## Adding References

### Edit YAML Directly (Recommended)

```bash
# Edit the file
open source/references.yaml

# Add your show to core or rotating_pool, then sync
./scripts/sync.sh
```

### Use the Interactive Skill (Claude Code)

```
/update-perfect-pair
```

## File Structure

```
perfect-pair-creator/
├── source/
│   ├── references.yaml              # Your reference library (EDIT THIS)
│   ├── config.yaml                  # Personality settings (EDIT THIS)
│   └── perfect-pair-base.md         # Template with {{PLACEHOLDER}} substitution
├── scripts/
│   ├── sync.sh                      # Main command (venv + build + deploy)
│   ├── build.py                     # Python build script (primary)
│   ├── deploy.sh                    # Deploy to all 4 tools
│   └── build.sh                     # Legacy (not used by sync)
├── generated/
│   ├── perfect-pair-current.md      # Auto-generated output
│   └── rotation-state.json          # Tracks active rotating refs
├── cursor-versions/
│   └── modern/.cursor/rules/        # Cursor formats and examples
└── skills/
    ├── update-perfect-pair/         # Interactive customization skill
    └── create-perfect-pair/         # Generate new styles skill
```

## Deploy Targets

### Cursor (Global Rules)
- Path: `~/.cursor/rules/perfect-pair.mdc`
- Format: Markdown with YAML frontmatter (`alwaysApply: true`)
- Applies to all projects automatically

### Claude Code (Plugin Hook)
- Path: `~/.claude/plugins/user/perfect-pair-output-style/`
- Format: SessionStart hook outputting JSON with `additionalContext`
- Restart Claude Code to see changes

### Gemini CLI (Global Context)
- Path: `~/.gemini/perfect-pair-style.md`
- Format: Plain markdown with `@import` in `~/.gemini/GEMINI.md`
- New sessions pick up changes automatically

### Codex CLI (Global Instructions)
- Path: `~/.codex/AGENTS.md`
- Format: Plain markdown (YAML frontmatter stripped)
- New sessions pick up changes automatically

## Requirements

- Python 3 (for build script)
- Bash (for deploy/sync scripts)
- At least one of: Cursor IDE, Claude Code CLI, Gemini CLI, Codex CLI

## Contributing

Have ideas? PRs welcome!

Ideas:
- Smart rotation implementation
- Usage tracking
- More pre-made styles
- Additional AI tool integrations

## License

MIT — Use it, share it, make it your own!

## Credits

Created because coding should be fun, and your programming partner should get your jokes.

Inspired by every dev who's ever said "I've made a huge mistake" while looking at their git diff.

---

**Quick Links:**
- [Workflow Guide](WORKFLOW.md)
- [Cursor Setup](cursor-versions/CURSOR-README.md)
- [GitHub Repo](https://github.com/joethorngren/perfect-pair)
