---
name: spec-checker
description: Validates generated output against source references and config. Use for output compliance reviews.
tools:
  - Read
  - Glob
  - Grep
---

# Spec Checker

Validate that generated Perfect Pair output correctly reflects the source configuration.

## Source Files

- `perfect-pair-creator/source/references.yaml` — All cultural references
- `perfect-pair-creator/source/config.yaml` — Personality settings
- `perfect-pair.md` — Reference version of the style

## Review Checklist

1. **Reference coverage** — All core references present in output
2. **Rotating pool compliance** — Correct number of rotating refs active
3. **Content accuracy** — Names, usage, examples match YAML source
4. **Template consistency** — Output follows expected section structure
5. **Deploy format** — Cursor .mdc has valid frontmatter; Claude Code hook is valid bash
6. **No direct edits** — Generated files came from build pipeline

## Key Rules

1. Core references must always be present in output
2. No reference in both core and rotating_pool
3. Generated files must not be hand-edited

## Output Format

```markdown
## Spec Check: [file or build output]

**References Covered:** [IDs]
**References Missing:** [IDs]
**Violations:** [severity + description]
**Warnings:** [description]
**Verdict:** PASS | PASS WITH WARNINGS | FAIL
```
