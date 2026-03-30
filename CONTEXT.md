# Animal Mixer — Development Context

## Overview
"Lillie's Animal Mixer!" — a browser-based animal mix-and-match game for kids (ages 3-8). Players pick body parts from different animals, add accessories, change backgrounds, and save creations to a shared gallery. Tablet-first, zero reading required.

The rubber ducky character was added for Maggie (Lillie's younger sister).

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
| Legs | y=320 to y=490 | Overlap with body bottom |
| Tails | y=200 to y=280 | Right side, x=280-380 |

### Accessory Anchor Points
| Accessory | Y Range | Notes |
|-----------|---------|-------|
| Hats/crown/bow/top hat/unicorn horn | y=0-60 | Top of head |
| Glasses | y=100-140 | Eye level |
| Bow tie | y=180-210 | Neck/upper chest |
| Elephant trunk | y=150-260 | Dangles from face |
| Frog tongue | y=160-270 | Extends from mouth |
| Dragon spikes | y=30-350 | Along spine center |
| Wings | y=180-300 | Mid-body, spread wide |

### Canvas Layer Order (bottom to top)
1. Background (full bleed)
2. Wings (behind body)
3. Body
4. Legs
5. Tail
6. Head
7. Dragon spikes (on top of body/head)
8. All other accessories (hats, glasses, etc. — topmost)

## SVG Art Style
- Nick Jr. cartoony: thick outlines (3-4px stroke), bold flat fills, NO gradients
- Slightly wobbly/hand-drawn feel
- Consistent color palettes per animal (see ANIMAL_MIXER_SPEC.md)
- Duck uses rubber ducky yellow #FFD700 / #FFC000

## Available Parts

| Category | Items |
|----------|-------|
| Heads (7) | tiger, elephant, monkey, frog, lion, deer, duck |
| Bodies (6) | tiger, elephant, bear, giraffe, panda, duck |
| Legs (6) | tiger, elephant, flamingo, frog, lion, duck |
| Tails (7) | tiger, peacock, lion, fish, snake, horse, duck |
| Accessories (11) | party_hat, crown, bow_tie, glasses, bow, top_hat, elephant_trunk, frog_tongue, unicorn_horn, dragon_spikes, wings |
| Backgrounds (6) | sky, jungle, desert, snowy, night, candy |

## Base Animal Presets
When a user picks a base animal, it maps to the best-matching parts:

| Base | Head | Body | Legs | Tail |
|------|------|------|------|------|
| Tiger | tiger | tiger | tiger | tiger |
| Elephant | elephant | elephant | elephant | fish |
| Bear | monkey | bear | lion | horse |
| Giraffe | deer | giraffe | flamingo | horse |
| Panda | frog | panda | duck | snake |
| Duck | duck | duck | duck | duck |

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
    /heads/       (7 SVGs)
    /bodies/      (6 SVGs)
    /legs/        (6 SVGs)
    /tails/       (7 SVGs)
    /accessories/ (11 SVGs)
  /backgrounds/   (6 SVGs)
```

## Deployment
- **Railway:** Auto-deploys from GitHub `main` branch
- **URL:** `https://animal-mixer-production.up.railway.app/mixer/`
- **Env vars needed:** `SUPABASE_URL`, `SUPABASE_ANON_KEY`

## Key Decisions & Fixes
- Supabase client variable renamed to `sbClient` to avoid collision with the CDN's global `window.supabase`
- Head necks removed — heads are just floating faces, bodies handle the torso connection
- Bodies positioned at y=150-380 (not y=80) to leave room for heads above
- Accessories realigned to match updated head (y=30-220) and body (y=150-380) positions
