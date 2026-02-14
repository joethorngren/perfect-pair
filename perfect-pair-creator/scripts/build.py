#!/usr/bin/env python3
"""
Build script for Perfect Pair style generator.
Reads references.yaml and generates the final style files.
"""

import yaml
import json
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
SOURCE_DIR = ROOT_DIR / "source"
GENERATED_DIR = ROOT_DIR / "generated"

REFERENCES_FILE = SOURCE_DIR / "references.yaml"
BASE_FILE = SOURCE_DIR / "perfect-pair-base.md"
ROTATION_STATE_FILE = GENERATED_DIR / "rotation-state.json"
OUTPUT_FILE = GENERATED_DIR / "perfect-pair-current.md"


def load_references():
    """Load the references library."""
    with open(REFERENCES_FILE, 'r') as f:
        return yaml.safe_load(f)


def load_rotation_state():
    """Load the current rotation state."""
    if ROTATION_STATE_FILE.exists():
        with open(ROTATION_STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_rotation": datetime.now().strftime("%Y-%m-%d"),
        "active_rotating_refs": [],
        "rotation_count": 0
    }


def generate_philosophy_opening(refs):
    """Generate the opening philosophy paragraph with references."""
    core_refs = refs['core']

    # Pick a few core references for the opening
    lines = []

    # Find specific references
    office = next((r for r in core_refs if r['name'] == 'The Office'), None)
    parks = next((r for r in core_refs if r['name'] == 'Parks & Rec'), None)
    arrested = next((r for r in core_refs if r['name'] == 'Arrested Development'), None)
    chappelle = next((r for r in core_refs if r['name'] == 'Dave Chappelle'), None)

    opening = []

    # Check rotating pool for Breaking Bad
    state = load_rotation_state()
    rotating_refs = [r for r in refs['rotating_pool'] if r['name'] in state['active_rotating_refs']]
    breaking_bad = next((r for r in rotating_refs if r['name'] == 'Breaking Bad'), None)

    if breaking_bad:
        opening.append("Like Walter White in the RV, you're meticulous about the process.")
    if parks:
        opening.append("Like Leslie Knope, you're passionate and organized.")
    if office:
        opening.append("Like Jim Halpert, you know when to question the absurd.")
    if chappelle:
        opening.append("Like Dave Chappelle, you're unafraid to speak truth.")
    if arrested:
        opening.append("And like the Bluths, you never miss an opportunity for a callback.")

    return " ".join(opening)


def generate_references_list(refs):
    """Generate the references list section."""
    core_refs = refs['core']
    state = load_rotation_state()
    active_rotating = [r for r in refs['rotating_pool'] if r['name'] in state['active_rotating_refs']]

    all_active = core_refs + active_rotating

    lines = []
    for ref in all_active:
        line = f"- **{ref['name']}**: {ref['usage']}"
        lines.append(line)

    return "\n".join(lines)


def generate_roast_examples(refs):
    """Generate roast examples using active references."""
    examples = []

    # Office example
    examples.append("""- User: "Let's just rewrite the entire codebase"
  You: "Okay, pump the brakes there, Leslie Knope. That's a lot of binders to organize. What specific pain point are we actually trying to solve? Let's start with one win instead of trying to fix all of Pawnee at once.\"""")

    examples.append("""- User: "I'll just add a quick try-catch around everything"
  You: "That's a bold strategy. But wrapping everything in try-catch is like Michael Scott's 'that's what she said' - seems to work everywhere until you realize you're just masking the real problems. Let's identify what could actually fail here.\"""")

    # Check if SNL is active
    state = load_rotation_state()
    if "SNL" in state['active_rotating_refs']:
        examples.append("""- User: "This should be fine, right?"
  You: "Weekend Update: 'Really?!' Let's actually check that assumption before we ship it and find out the hard way.\"""")

    # Check if Key & Peele is active
    if "Key & Peele" in state['active_rotating_refs']:
        examples.append("""- User: "I'm going to optimize everything!"
  You: "Whoa there, calm down. You're like A-Aron from Key & Peele - you done messed up. Premature optimization is the root of all evil. Let's measure first, then optimize what actually matters.\"""")

    return "\n\n".join(examples)


def build_style():
    """Build the complete style file."""
    print("🔨 Building Perfect Pair style...")

    # Load data
    refs = load_references()

    # Load base template
    with open(BASE_FILE, 'r') as f:
        base_content = f.read()

    # Generate sections
    philosophy = generate_philosophy_opening(refs)
    references_list = generate_references_list(refs)
    roast_examples = generate_roast_examples(refs)

    # Replace placeholders
    output = base_content.replace("{{PHILOSOPHY_OPENING}}", philosophy)
    output = output.replace("{{REFERENCES_LIST}}", references_list)
    output = output.replace("{{ROAST_EXAMPLES}}", roast_examples)

    # Write output
    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)

    print(f"✅ Generated: {OUTPUT_FILE}")

    # Print stats
    state = load_rotation_state()
    print(f"\n📊 Active references:")
    print(f"   Core: {len(refs['core'])}")
    print(f"   Rotating: {len(state['active_rotating_refs'])}/{len(refs['rotating_pool'])}")
    print(f"   Total: {len(refs['core']) + len(state['active_rotating_refs'])}")
    print(f"\n🔄 Currently active rotating refs:")
    for ref_name in state['active_rotating_refs']:
        print(f"   - {ref_name}")


if __name__ == "__main__":
    build_style()
