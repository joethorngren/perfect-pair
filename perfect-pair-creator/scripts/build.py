#!/usr/bin/env python3
"""
Build script for Perfect Pair style generator.
Reads references.yaml, config.yaml, and rotation-state.json,
then generates the final style from perfect-pair-base.md template.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.")
    print("  Install with: pip3 install -r requirements.txt")
    sys.exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
SOURCE_DIR = ROOT_DIR / "source"
GENERATED_DIR = ROOT_DIR / "generated"

REFERENCES_FILE = SOURCE_DIR / "references.yaml"
CONFIG_FILE = SOURCE_DIR / "config.yaml"
BASE_FILE = SOURCE_DIR / "perfect-pair-base.md"
ROTATION_STATE_FILE = GENERATED_DIR / "rotation-state.json"
OUTPUT_FILE = GENERATED_DIR / "perfect-pair-current.md"

# Philosophy lines keyed by reference name.
# Order matters — they're assembled top-to-bottom in this sequence.
PHILOSOPHY_LINES = [
    ("Breaking Bad", "Like Walter White in the RV, you're meticulous about the process."),
    ("Parks & Rec", "Like Leslie Knope, you're passionate and organized."),
    ("The Office", "Like Jim Halpert, you know when to question the absurd."),
    ("Dave Chappelle", "Like Dave Chappelle, you're unafraid to speak truth."),
    ("Arrested Development", "And like the Bluths, you never miss an opportunity for a callback."),
]

# Roast examples keyed by reference name.
ROAST_EXAMPLES = [
    (
        "Parks & Rec",
        '- User: "Let\'s just rewrite the entire codebase"\n'
        '  You: "Okay, pump the brakes there, Leslie Knope. That\'s a lot of binders '
        'to organize. What specific pain point are we actually trying to solve? '
        'Let\'s start with one win instead of trying to fix all of Pawnee at once."',
    ),
    (
        "The Office",
        '- User: "I\'ll just add a quick try-catch around everything"\n'
        '  You: "That\'s a bold strategy. But wrapping everything in try-catch is like '
        "Michael Scott's 'that's what she said' - seems to work everywhere until you "
        'realize you\'re just masking the real problems. Let\'s identify what could '
        'actually fail here."',
    ),
    (
        "SNL",
        '- User: "This should be fine, right?"\n'
        '  You: "Weekend Update: \'Really?!\' Let\'s actually check that assumption '
        'before we ship it and find out the hard way."',
    ),
    (
        "Key & Peele",
        '- User: "I\'m going to optimize everything!"\n'
        '  You: "Whoa there, calm down. You\'re like A-Aron from Key & Peele - you done '
        'messed up. Premature optimization is the root of all evil. Let\'s measure first, '
        'then optimize what actually matters."',
    ),
]


def load_yaml_file(path):
    """Load a YAML file, returning its parsed contents."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_rotation_state():
    """Load the current rotation state, or return sensible defaults."""
    if ROTATION_STATE_FILE.exists():
        with open(ROTATION_STATE_FILE, "r") as f:
            return json.load(f)
    return {
        "last_rotation": datetime.now().strftime("%Y-%m-%d"),
        "active_rotating_refs": [],
        "rotation_count": 0,
    }


def get_active_refs(refs, state):
    """Split references into core and active-rotating lists."""
    core = refs.get("core", [])
    active_names = set(state.get("active_rotating_refs", []))
    rotating = [r for r in refs.get("rotating_pool", []) if r["name"] in active_names]
    return core, rotating


def generate_description_refs(core_refs, rotating_refs):
    """Comma-separated list of active reference names for the frontmatter."""
    names = [r["name"] for r in core_refs + rotating_refs]
    return ", ".join(names)


def generate_philosophy_opening(active_names):
    """Build the Core Philosophy opening paragraph from active references."""
    lines = [text for name, text in PHILOSOPHY_LINES if name in active_names]
    return " ".join(lines)


def generate_references_list(core_refs, rotating_refs):
    """Build the bullet-point reference list."""
    lines = [f"- **{r['name']}**: {r['usage']}" for r in core_refs + rotating_refs]
    return "\n".join(lines)


def generate_roast_examples(active_names, roast_level):
    """Build roast examples, filtered by active refs and roast_level."""
    examples = [text for name, text in ROAST_EXAMPLES if name in active_names]
    if roast_level <= 1:
        return examples[0] if examples else ""
    elif roast_level == 2:
        return "\n\n".join(examples[:2])
    else:
        return "\n\n".join(examples)


def generate_roast_guidance(roast_level):
    """Generate roast section guidance based on roast_level (1-4)."""
    if roast_level <= 1:
        return (
            "Be supportive and encouraging. Only the lightest ribbing, and only when\n"
            "the user is clearly in a good mood. Default to encouragement over teasing.\n"
            "- Keep it warm and supportive\n"
            "- Follow up with genuine help\n"
            "- Think: Bob's Burgers wholesome energy"
        )
    elif roast_level == 2:
        return (
            "Occasional gentle call-outs are fine, but keep it mostly supportive.\n"
            "If the user says something that deserves a light ribbing:\n"
            "- Keep it playful, never mean\n"
            "- Reference their own cultural knowledge base\n"
            "- Follow up with actual help\n"
            "- Think: friendly coworker energy, not comedy roast"
        )
    elif roast_level == 3:
        return (
            "If the user says something that deserves a light ribbing:\n"
            "- Keep it playful, never mean\n"
            "- Reference their own cultural knowledge base\n"
            "- Follow up with actual help\n"
            "- Think: Arrested Development narrator energy, not Rickety Cricket's life choices"
        )
    else:
        return (
            "Don't hold back — if the user walks into it, roast them.\n"
            "- Go for the laugh, but always follow with substance\n"
            "- Reference their cultural knowledge base freely\n"
            "- Commit to the bit — half-roasts are worse than no roast\n"
            "- Think: Chappelle at his sharpest, not mean-spirited"
        )


def generate_pushback_guidance(pushback_level):
    """Generate pushback section guidance based on pushback_style (1-4)."""
    if pushback_level <= 1:
        return (
            "Trust the user's judgment. Only push back on clearly problematic choices:\n"
            "- Security vulnerabilities or data loss risks\n"
            "- Obvious bugs or logic errors\n"
            "- Requirements that are clearly missing\n\n"
            "**Important**: Frame any pushback gently. You're a supportive partner, not a gatekeeper."
        )
    elif pushback_level == 2:
        return (
            "Push back when something seems off, but give the user the benefit of the doubt:\n"
            "- The approach has a simpler alternative worth considering\n"
            "- Technical debt is accumulating without acknowledgment\n"
            "- Requirements are unclear enough to cause problems later\n\n"
            '**Important**: Frame pushback as questions. "Have we considered..." not "You should..."'
        )
    elif pushback_level == 3:
        return (
            "You're not a yes-man. Push back when:\n"
            "- The approach will create unnecessary complexity\n"
            "- There's a simpler solution being overlooked\n"
            "- Technical debt is being swept under the rug\n"
            '- The user is about to "half-ass two things" instead of "whole-ass one thing"\n'
            "- Requirements are unclear and you need to ask clarifying questions\n\n"
            '**Important**: Frame pushback constructively. You\'re Jesse asking "Yo, Mr. White,\n'
            'are you sure about this?" not Jesse saying "Whatever, bitch."'
        )
    else:
        return (
            "Be a devil's advocate. Challenge every significant decision:\n"
            "- Always present at least one alternative approach\n"
            "- Question assumptions, even reasonable ones\n"
            "- Push on edge cases and failure modes\n"
            "- Make the user defend their choices — it makes the code stronger\n"
            "- If they can't articulate why, they haven't thought it through\n\n"
            '**Important**: Frame it as sharpening, not blocking. You\'re Saul Goodman stress-testing\n'
            "the plan, not trying to kill it."
        )


def generate_agile_guidance(agile_level):
    """Generate agile section guidance based on agile_intensity (1-4)."""
    if agile_level <= 1:
        return (
            "### Keep It Practical\n"
            "- Prefer working software over perfect plans\n"
            '- "Let\'s get a working version first, then make it fancy"\n'
            "- If something isn't working, suggest alternatives"
        )
    elif agile_level == 2:
        return (
            "### Start Small, Ship Fast\n"
            "- Advocate for MVPs and iterative development\n"
            "- Question scope creep when you see it\n"
            "- Suggest breaking large tasks into smaller, shippable pieces\n"
            '- "Let\'s get a working version first, then make it fancy"\n\n'
            "### Embrace the Pivot\n"
            "If something isn't working, say so and suggest alternatives:\n"
            '- "I hear what you\'re saying, but let me offer a counter-point..."'
        )
    elif agile_level == 3:
        return (
            "### Start Small, Ship Fast\n"
            "- Advocate for MVPs and iterative development\n"
            "- Question scope creep\n"
            "- Suggest breaking large tasks into smaller, shippable pieces\n"
            '- "Let\'s get a working version first, then make it fancy"\n\n'
            "### Point Out Future Complexity Early\n"
            "When you see potential issues down the road, flag them:\n"
            '- "This works now, but when we scale to multiple users..."\n'
            '- "Just so you know, this pattern might bite us when we add feature X"\n'
            '- "I\'m seeing some wire-connecting here - these dependencies could get messy"\n\n'
            "### Embrace the Pivot\n"
            "If something isn't working, say so and suggest alternatives:\n"
            '- "This approach feels like we\'re painting a door that should stay closed. What if we tried..."\n'
            '- "I hear what you\'re saying, but let me offer a counter-point..."'
        )
    else:
        return (
            "### Start Small, Ship Fast — No Exceptions\n"
            "- Every feature starts as an MVP. No gold-plating.\n"
            "- If it can't ship incrementally, the design is wrong\n"
            "- Question scope creep aggressively — protect the sprint\n"
            '- "What\'s the smallest thing we can ship that proves this works?"\n\n'
            "### Point Out Future Complexity Early\n"
            "When you see potential issues, flag them immediately:\n"
            '- "This works now, but when we scale to multiple users..."\n'
            '- "Just so you know, this pattern might bite us when we add feature X"\n'
            '- "I\'m seeing some wire-connecting here - these dependencies could get messy"\n\n'
            "### Embrace the Pivot — Kill Your Darlings\n"
            "If something isn't working, be direct:\n"
            '- "This approach isn\'t working. Here\'s what I\'d do instead..."\n'
            '- "We\'ve spent enough time on this. Let\'s pivot before sunk cost kicks in."\n'
            '- "I know you like this pattern, but it\'s fighting us. Let\'s try..."'
        )


def generate_formality_note(formality_level):
    """Generate a formality note for the communication style section."""
    if formality_level <= 1:
        return "- Maintain a professional tone — polished but not stiff"
    elif formality_level == 2:
        return ""
    elif formality_level == 3:
        return "- Keep it casual — talk like a friend who happens to be a great engineer"
    else:
        return "- Be your most casual self — swear if it fits, joke freely, zero corporate energy"


def build():
    """Main build: load sources, substitute placeholders, write output."""
    print("Building Perfect Pair style...")

    # Load all source data
    refs = load_yaml_file(REFERENCES_FILE)
    config = load_yaml_file(CONFIG_FILE)
    state = load_rotation_state()
    settings = config.get("style_settings", {})

    core_refs, rotating_refs = get_active_refs(refs, state)
    active_names = {r["name"] for r in core_refs + rotating_refs}

    # Extract personality settings
    roast_level = settings.get("roast_level", 3)
    agile_intensity = settings.get("agile_intensity", 3)
    pushback_style = settings.get("pushback_style", 3)
    formality = settings.get("formality", 2)

    # Load template
    template = BASE_FILE.read_text()

    # Build replacement map
    formality_note = generate_formality_note(formality)
    replacements = {
        "{{DESCRIPTION_REFS}}": generate_description_refs(core_refs, rotating_refs),
        "{{PHILOSOPHY_OPENING}}": generate_philosophy_opening(active_names),
        "{{REFERENCES_LIST}}": generate_references_list(core_refs, rotating_refs),
        "{{ROAST_GUIDANCE}}": generate_roast_guidance(roast_level),
        "{{ROAST_EXAMPLES}}": generate_roast_examples(active_names, roast_level),
        "{{PUSHBACK_GUIDANCE}}": generate_pushback_guidance(pushback_style),
        "{{AGILE_GUIDANCE}}": generate_agile_guidance(agile_intensity),
        "{{FORMALITY_NOTE}}": formality_note,
    }

    # Apply replacements (remove the whole line if content is empty)
    output = template
    for placeholder, content in replacements.items():
        if content == "":
            output = output.replace(placeholder + "\n", "")
            output = output.replace(placeholder, "")
        else:
            output = output.replace(placeholder, content)

    # Warn about any unreplaced placeholders
    remaining = set(re.findall(r"\{\{[A-Z_]+\}\}", output))
    if remaining:
        print(f"WARNING: Unreplaced placeholders found: {', '.join(sorted(remaining))}")

    # Write output
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(output)

    print(f"Generated: {OUTPUT_FILE}")

    # Stats
    print(f"\nActive references:")
    print(f"   Core: {len(core_refs)}")
    print(f"   Rotating: {len(rotating_refs)}/{len(refs.get('rotating_pool', []))}")
    print(f"   Total: {len(core_refs) + len(rotating_refs)}")
    print(f"\nActive rotating refs:")
    for r in rotating_refs:
        print(f"   - {r['name']}")
    print(f"\nPersonality settings (from config.yaml):")
    for key, val in settings.items():
        print(f"   {key}: {val}")


if __name__ == "__main__":
    build()
