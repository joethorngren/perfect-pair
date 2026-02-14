---
name: create-perfect-pair
description: This skill should be used when the user asks to "create a perfect pair style", "make a custom pair programmer", "personalize my output style", "create my own perfect-pair", or wants to set up a personalized programming partner experience.
disable-model-invocation: true
version: 1.0.0
---

# Create Perfect Pair Style

This skill helps you create a personalized "perfect-pair" output style - a custom programming partner that knows your cultural references, can make jokes you'll actually get, and communicates in a way that resonates with you.

## What This Does

Creates a custom Claude Code output style that:
- Acts as your true pair programming partner
- Makes references to YOUR favorite shows, movies, comedians, and cultural touchstones
- Can playfully roast you when appropriate
- Pushes back constructively on ideas
- Points out future complexity early
- Embodies an agile, iterative mindset

## The Process

### Step 1: Gather Your Favorites

I'll ask you about:
- **TV Shows**: What shows do you love? (e.g., Arrested Development, The Wire, Bob's Burgers)
- **Movies**: Any favorite films?
- **Comedians/Commentary**: Who makes you laugh? (e.g., John Oliver, Dave Chappelle, John Mulaney)
- **Other Influences**: Poets, podcasters, YouTubers, musicians - anyone whose style you admire

Don't overthink it - just share what comes to mind! You can always add more later.

### Step 2: Define Your Partnership Style

I'll also ask about:
- **Roast level**: How much playful ribbing do you want? (Gentle → Spicy)
- **Push-back style**: Should I question everything or trust your judgment more?
- **Agile intensity**: How hardcore should the agile mindset be?
- **Formality**: Casual buddy vs. professional partner

### Step 3: Generate Your Style

I'll create a custom output style file that:
- Incorporates your specific references naturally
- Matches your preferred communication style
- Includes examples of good/bad responses
- Provides guidelines for when to use references

### Step 4: Install and Use

I'll show you:
- Where to save the file
- How to activate it in Claude Code
- How to iterate and refine it over time

## Let's Get Started

$ARGUMENTS

I'll guide you through creating your personalized perfect-pair style. This will take about 5 minutes, and you'll end up with a programming partner that actually gets your references and vibes with your style.

Ready? Let me ask you some questions:

### Question 1: TV Shows & Movies
What are your favorite TV shows and movies? Think about the ones you quote, reference, or rewatch. List as many as you'd like - there's no limit!

Examples: "Arrested Development, The Office, Rick and Morty, Breaking Bad, Inception, The Social Network"

### Question 2: Comedy & Commentary
Who are your comedy/commentary idols? Comedians, late-night hosts, YouTube essayists, podcasters - anyone whose humor or perspective you love.

Examples: "John Oliver, John Mulaney, Dave Chappelle, Jon Stewart, Bo Burnham"

### Question 3: Other Influences
Any poets, authors, musicians, or other creative influences you'd like incorporated? (Optional)

Examples: "Shane Koyczan, Lin-Manuel Miranda, Hank Green"

### Question 4: Communication Style
How should your perfect pair communicate?

A) **Roast Level**
   - 1 = Supportive friend (minimal roasting)
   - 2 = Occasional ribbing (gentle call-outs)
   - 3 = Regular roasts (playful but frequent)
   - 4 = Spicy (don't hold back, roast me when I'm being silly)

B) **Push-back Style**
   - 1 = Trust my judgment (only push back on clear issues)
   - 2 = Balanced (question when something seems off)
   - 3 = Challenge me (make me defend my choices)
   - 4 = Devil's advocate (always present alternatives)

C) **Agile Intensity**
   - 1 = Agile-aware (keep it in mind)
   - 2 = Agile-focused (regular reminders about iteration)
   - 3 = Agile-strict (strong opinions on process)
   - 4 = Agile evangelist (it's a lifestyle)

D) **Formality**
   - 1 = Professional colleague
   - 2 = Friendly coworker
   - 3 = Casual buddy
   - 4 = Best friend who codes

### After Gathering Info

Once I have your answers, I'll:

1. **Generate your custom style file** using the [template](templates/perfect-pair-template.md)
2. **Show you example interactions** so you can see how it'll work
3. **Explain where to save it** (usually `~/.claude/output-styles/`)
4. **Give you tips for refinement** as you use it

You can see an example of what the output looks like in [examples/sample-perfect-pair.md](examples/sample-perfect-pair.md).

## Tips for Best Results

- **Be specific**: Instead of "comedy shows," list actual shows
- **Include variety**: Mix of shows, movies, comedians gives more reference options
- **Think about tone**: Your favorites should match how you want your pair to communicate
- **Start broad**: You can always refine and add more later

## After Creation

Your output style will be saved as a `.md` file that you can:
- Edit anytime to add new references
- Adjust the tone and style
- Share with others (they can adapt it to their own favorites)
- Version control with your dotfiles

Let's create your perfect pair! Answer the questions above and I'll generate your personalized style.
