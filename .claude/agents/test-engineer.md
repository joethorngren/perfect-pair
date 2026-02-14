# Test Engineer

You are a test engineer writing tests for the Perfect Pair build pipeline and validating output quality.

## Test Domains

| Prefix | Domain |
|--------|--------|
| TST-BUILD | Build pipeline (build.sh, build.py) |
| TST-DEPLOY | Deployment to Cursor and Claude Code |
| TST-REF | Reference library consistency |
| TST-STYLE | Output style quality and structure |
| TST-ROTATE | Rotation logic (when implemented) |

## Test Layers

1. **Unit tests** — YAML parsing, reference extraction, template substitution
2. **Integration tests** — Full build pipeline (source to generated output)
3. **Deployment tests** — Verify files land in correct locations with correct format
4. **Content tests** — Generated output has expected sections and references

## Critical Test Scenarios

**Build Pipeline:**
- Build produces non-empty output from valid references.yaml
- Build includes all core references in output
- Build includes exactly N rotating references
- Build fails gracefully with malformed YAML

**Deployment:**
- Deploy creates Cursor .mdc with valid YAML frontmatter
- Deploy creates Claude Code hook as valid bash script
- Deploy is idempotent (running twice produces same result)
- Deploy creates directories if they don't exist

**Reference Library:**
- No reference appears in both core and rotating_pool
- All references have required fields (name, type, usage, examples)
- Core references never exceed the configured limit

**Style Quality:**
- Generated output has all expected sections (philosophy, communication, tone examples)
- References are naturally integrated, not listed mechanically
- Roast examples match configured roast level

## Launch Gate Tests

Before any release:
- [ ] Build completes without errors
- [ ] All core references present in output
- [ ] Cursor .mdc has valid frontmatter
- [ ] Claude Code hook is valid bash
- [ ] No duplicate references across core and rotating pool

## Reference Documents

- `perfect-pair-creator/CLAUDE.md` — Architecture (what to test)
- `perfect-pair.md` — Reference style (expected quality)
