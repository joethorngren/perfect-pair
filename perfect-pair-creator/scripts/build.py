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


def generate_roast_examples(active_names):
    """Build roast examples, including only those whose reference is active."""
    examples = [text for name, text in ROAST_EXAMPLES if name in active_names]
    return "\n\n".join(examples)


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

    # Load template
    template = BASE_FILE.read_text()

    # Build replacement map
    replacements = {
        "{{DESCRIPTION_REFS}}": generate_description_refs(core_refs, rotating_refs),
        "{{PHILOSOPHY_OPENING}}": generate_philosophy_opening(active_names),
        "{{REFERENCES_LIST}}": generate_references_list(core_refs, rotating_refs),
        "{{ROAST_EXAMPLES}}": generate_roast_examples(active_names),
    }

    # Apply replacements
    output = template
    for placeholder, content in replacements.items():
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
