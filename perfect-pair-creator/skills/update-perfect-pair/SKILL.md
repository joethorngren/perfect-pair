---
name: add-reference
description: This skill should be used when the user wants to "add a reference", "add a new show", "add a movie to perfect pair", "update my references", or wants to add cultural references to their Perfect Pair style.
disable-model-invocation: true
version: 1.0.0
---

# Add Reference to Perfect Pair

This skill helps you quickly add new shows, movies, comedians, or other cultural references to your Perfect Pair style.

## What This Does

Guides you through adding a new reference to `source/references.yaml` and automatically syncs it to all your editors.

## The Process

I'll ask you a few quick questions:

### Question 1: What are you adding?

**Name**: What show, movie, comedian, or cultural reference?

Examples: "Community", "30 Rock", "Bo Burnham", "The Matrix"

### Question 2: What type is it?

- **show** - TV show
- **movie** - Film
- **comedian** - Stand-up comedian or comedy personality
- **podcast** - Podcast
- **other** - YouTube channel, poet, musician, etc.

### Question 3: When should it be used?

**Usage**: Describe when/how to reference this in code conversations.

Examples:
- "Meta discussions, 'cool cool cool' moments"
- "Existential questions, red pill/blue pill decisions"
- "Inside-out perspectives on code architecture"

Be specific about the context, tone, or situations where this reference fits.

### Question 4: Example quotes or situations?

Give 1-2 examples of specific quotes, moments, or ways to use this reference.

Examples:
- "Cool cool cool"
- "Red pill or blue pill moment"
- "There are no accidents - Master Oogway"

### Question 5: Core or rotating?

**Core** - Always included (reserved for your absolute favorites)
- Current core: The Office, Parks & Rec, Arrested Development, Dave Chappelle

**Rotating Pool** - Rotates in and out to manage context
- Recommended for most new additions
- Currently 5 active at a time from the pool

Choose:
- **core** - If this is a top-tier favorite you want always present
- **rotating** - For everything else (recommended)

## After You Answer

I will:

1. **Validate** your input
2. **Update** `source/references.yaml` with the new reference
3. **Run** `./scripts/sync.sh` to deploy everywhere
4. **Confirm** what was added and where it's active

## Example Interaction

**User**: "Add Community to my references"

**Assistant**:
"Great! Let me add Community to your Perfect Pair references.

I'll need a few details:

1. **Name**: Community ✓
2. **Type**: show ✓
3. **Usage**: How should I describe when to use Community references?
   (e.g., 'Meta discussions, study group dynamics, cool cool cool moments')

4. **Examples**: Any specific quotes or moments?
   (e.g., 'Cool cool cool', 'Abed's meta commentary', 'Six seasons and a movie')

5. **Add to**:
   - Core (always included - for top favorites)
   - Rotating (recommended - rotates weekly)

Which would you prefer?"

## Technical Implementation

When executed, this skill will:

```bash
# 1. Read current references.yaml
# 2. Add new entry in proper YAML format
# 3. Validate YAML syntax
# 4. Write updated file
# 5. Run sync script
# 6. Report success
```

## Tips

- **Be specific** about usage - helps me know when to use it
- **Add to rotating** unless it's truly top-tier
- **Multiple examples** are helpful but not required
- **Edit anytime** - You can always refine in references.yaml

## Important Notes

- This skill requires the perfect-pair-creator repo to be set up
- The repo should be at: `/Users/oh_henry/Code_Complete/perfect-pair/perfect-pair-creator/`
- If the path is different, let me know and I'll update accordingly

## After Adding

Your new reference will be:
- ✅ In `source/references.yaml`
- ✅ Deployed to Cursor (global rules)
- ✅ Deployed to Claude Code (plugin)
- ✅ Available immediately (after restart)

Ready to add a new reference? Let's do it! 🎬
