# Animal Mixer — Development Context

## Overview
"Lillie's Animal Mixer!" — a browser-based animal mix-and-match game for kids (ages 3-8). Players pick body parts from different animals, add accessories, change backgrounds, and save creations to a shared gallery. Tablet-first, zero reading required.

- The rubber ducky character was added for Maggie (Lillie's younger sister).
- The knight and dragon were added at Lillie's request for medieval play combos.
- Flamingo was added as a full base animal.

## Tech Stack
- **Frontend:** Single-file vanilla HTML/CSS/JS (`index.html`), no framework/build step
- **Rendering:** Layered SVG parts stacked absolutely inside a 400x500 canvas div
- **Photo capture:** html2canvas library -> PNG blob
- **Backend:** FastAPI on Railway (`main.py`) serving static files at `/mixer`
- **Storage + gallery:** Supabase — `animal-mixer` storage bucket + `animal_mixer_saves` table
- **Config injection:** FastAPI endpoint `/mixer/config.js` injects `SUPABASE_URL` and `SUPABASE_ANON_KEY`

## SVG Part System — Coordinate Reference

All parts use `viewBox="0 0 400 500"`, centered at x=200.

| Layer | Y Range | Notes |
|-------|---------|-------|
| Heads | y=30 to y=220 | Face/features only, NO neck stub |
| Bodies | y=150 to y=380 | ~180-220px wide, shoulders at ~y=150 |
| Arms | y=170 to y=320 | Left arm x=70-120, right arm x=280-330 |
| Legs | y=320 to y=490 | Overlap with body bottom |
| Tails | y=200 to y=280 | Right side, x=280-380 |

### Accessory Anchor Points
| Accessory | Y Range | Notes |
|-----------|---------|-------|
| Hats/crown/bow/top hat/unicorn horn | y=0-60 | Top of head |
| Glasses | y=100-140 | Eye level |
| Bow tie | y=180-210 | Neck/upper chest |
| Elephant trunk | y=150-260 | Dangles from face |
| Frog tongue | y=220-340 | Extends below head/mouth |
| Dragon spikes | y=0-88 | Branching moose-like horns from head area |
| Wings | y=180-300 | Mid-body, spread wide |
| Shield | x=50-140, y=180-310 | Left side, mid-body |
| Sword | x=270-370, y=120-310 | Right side, angled heroically |

### Canvas Layer Order (bottom to top)
1. Background (full bleed)
2. Wings (behind body)
3. Tail (behind body)
4. Body
5. Arms
6. Legs
7. Head
8. Dragon spikes (on top of body/head)
9. All other accessories (hats, glasses, shield, sword, etc. — topmost)

## SVG Art Style
- Nick Jr. cartoony: thick outlines (3-4px stroke), bold flat fills, NO gradients
- Slightly wobbly/hand-drawn feel
- Consistent color palettes per animal (see ANIMAL_MIXER_SPEC.md)
- Duck: rubber ducky yellow #FFD700 / #FFC000
- Dragon: purple #7B68EE / #6A5ACD, green belly #98FB98, gold horns/claws #FFD700
- Knight: silver armor #B0B0B0 / #808080, gold trim #FFD700, red accents #FF3333
- Flamingo: pink #FF69B4 / #FF1493

## Available Parts

| Category | Count | Items |
|----------|-------|-------|
| Heads | 10 | tiger, elephant, monkey, frog, lion, deer, duck, dragon, knight, flamingo |
| Bodies | 9 | tiger, elephant, bear, giraffe, panda, duck, dragon, flamingo, knight |
| Arms | 12 | tiger, elephant, monkey, frog, lion, deer, duck, dragon, bear, giraffe, panda, flamingo, knight |
| Legs | 8 | tiger, elephant, flamingo, frog, lion, duck, dragon, knight |
| Tails | 10 | tiger, peacock, lion, fish, snake, horse, duck, dragon, flamingo, knight |
| Accessories | 13 | party_hat, crown, bow_tie, glasses, bow, top_hat, elephant_trunk, frog_tongue, unicorn_horn, dragon_spikes, wings, shield, sword |
| Backgrounds | 6 | sky, jungle, desert, snowy, night, candy |

## Base Animal Presets (9)
When a user picks a base animal, it maps to the best-matching parts:

| Base | Head | Body | Arms | Legs | Tail |
|------|------|------|------|------|------|
| Tiger | tiger | tiger | tiger | tiger | tiger |
| Elephant | elephant | elephant | elephant | elephant | fish |
| Bear | monkey | bear | bear | lion | horse |
| Giraffe | deer | giraffe | giraffe | flamingo | horse |
| Panda | frog | panda | panda | duck | snake |
| Duck | duck | duck | duck | duck | duck |
| Dragon | dragon | dragon | dragon | dragon | dragon |
| Flamingo | flamingo | flamingo | flamingo | flamingo | flamingo |
| Knight | knight | knight | knight | knight | knight |

## File Structure
```
/animal-mixer/
  index.html          <- entire game (single file)
  main.py             <- FastAPI backend for Railway
  requirements.txt    <- fastapi, uvicorn
  Procfile            <- Railway deployment
  ANIMAL_MIXER_SPEC.md <- original spec
  CONTEXT.md          <- this file
  /parts/
    /heads/       (10 SVGs)
    /bodies/      (9 SVGs)
    /arms/        (12 SVGs)
    /legs/        (8 SVGs)
    /tails/       (10 SVGs)
    /accessories/ (13 SVGs)
  /backgrounds/   (6 SVGs)
```

## Deployment
- **Railway:** Auto-deploys from GitHub `main` branch
- **URL:** `https://animal-mixer-production.up.railway.app/mixer/`
- **Env vars needed:** `SUPABASE_URL`, `SUPABASE_ANON_KEY`
- **GitHub:** `https://github.com/mitch-coluzzi/animal-mixer`

## Key Decisions & Fixes
- Supabase client variable renamed to `sbClient` to avoid collision with the CDN's global `window.supabase`
- Head necks removed — heads are just floating faces, bodies handle the torso connection
- Bodies positioned at y=150-380 (not y=80) to leave room for heads above
- Accessories realigned to match updated head (y=30-220) and body (y=150-380) positions
- Arms are a separate mixable layer (not baked into bodies) for mix-and-match
- Tails render behind body layer so they peek out from behind
- Dragon teeth reduced from 3 to 2 small fangs to avoid looking like dots
- Dragon spikes redesigned as branching moose-like horns at head level
- Elephant head redone with huge Dumbo-style floppy ears
- Knight tail is a flowing red cape
- Sidebar uses flex-shrink:0 to prevent overlap with stage
- Base picker wraps to handle 9+ animals
- Supabase storage needs RLS policies for public upload/read on `animal-mixer` bucket
- Clear button resets all parts, accessories, and background to empty state
