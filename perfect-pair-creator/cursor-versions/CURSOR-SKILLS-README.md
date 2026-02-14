# Perfect Pair Cursor Skills (v2.4+)

For Cursor 2.4 and later, you can use the interactive skill to generate your own personalized perfect-pair style!

## What's the Difference?

**Rules** (`.cursorrules` / `.cursor/rules/`) - Always-on behavior
- Pre-made personality based on specific shows/comedians
- Works immediately, no setup
- Good for: Quick start, sharing with team, consistent behavior

**Skills** (`cursor/skills/`) - Interactive generator (Cursor 2.4+)
- Guides you through creating YOUR custom style
- Asks about YOUR favorite shows and preferences
- Generates personalized rules files
- Good for: Customization, making it truly yours

## Installation

### Copy the Skill to Your Project

```bash
# From the perfect-pair-creator directory
cp -r cursor-versions/skills/create-perfect-pair cursor/skills/
```

Or for global installation (if Cursor supports it):
```bash
cp -r cursor-versions/skills/create-perfect-pair ~/.cursor/skills/
```

## Usage

Once installed, the skill will be automatically discovered by Cursor 2.4+.

### Invoke It

Just ask Cursor:
- "Create a custom cursor style"
- "I want to personalize my AI partner"
- "Make cursor more fun with my favorite shows"
- "Generate a perfect-pair style for me"

Or reference it directly if Cursor supports skill invocation.

### The Process

The skill will guide you through:

1. **Your favorite shows/movies** - List what you love
2. **Comedy/commentary idols** - Who makes you laugh?
3. **Other influences** - Poets, musicians, etc. (optional)
4. **Style preferences** - Roast level, push-back style, agile intensity, formality

Then it generates both:
- `.cursorrules` (legacy format)
- `.cursor/rules/perfect-pair.mdc` (modern format)

With YOUR references and YOUR preferred communication style!

## File Structure

```
your-project/
└── cursor/
    └── skills/
        └── create-perfect-pair/
            ├── SKILL.md                      # The interactive skill
            ├── templates/
            │   └── perfect-pair-template.md  # Template for generation
            └── examples/
                └── sample-perfect-pair.md    # Example output
```

## For Older Cursor Versions (Pre-2.4)

If you don't have Cursor 2.4, you can still:

1. **Use the pre-made rules** - See the main CURSOR-README.md
2. **Manually customize** - Use CUSTOMIZATION-TEMPLATE.md as a guide
3. **Wait for Cursor 2.4** - Then come back and use the skill!

## Comparison: Skills vs Rules

| Feature | Pre-made Rules | Interactive Skill |
|---------|---------------|-------------------|
| Setup time | Instant | 5 minutes |
| Customization | Manual editing | Guided questions |
| References | Pre-set shows | YOUR shows |
| Cursor version | Any | 2.4+ |
| Team sharing | Easy | Generate once, share result |

## Tips

- **Try the pre-made rules first** to see if you like the concept
- **Use the skill to customize** if you want different references
- **Share the generated rules** with your team (commit the `.cursor` folder)
- **Iterate** - You can re-run the skill or manually edit anytime

## Troubleshooting

**Skill not being discovered?**
- Make sure you're on Cursor 2.4 or later
- Check that `SKILL.md` is in the right location
- Try restarting Cursor

**Want to regenerate?**
- Delete your existing `.cursorrules` or `.cursor/rules/perfect-pair.mdc`
- Invoke the skill again with new answers

**Prefer manual customization?**
- Use the CUSTOMIZATION-TEMPLATE.md guide
- Edit the rules files directly

## What Gets Generated

The skill creates a complete Cursor rules file that:
- Opens with references to YOUR favorite shows
- Includes a guide for when to use YOUR references
- Has roast examples using YOUR cultural touchstones
- Matches YOUR preferred communication style
- Embodies YOUR desired agile intensity

All tuned specifically to what you told the skill!

## Next Steps

1. Install the skill (copy to `cursor/skills/`)
2. Invoke it in Cursor 2.4+
3. Answer the 4 questions
4. Get your personalized rules files
5. Code with a partner that actually gets your jokes!

---

**Note:** This is for Cursor IDE. For Claude Code, use the skill in `skills/create-perfect-pair/` instead.
