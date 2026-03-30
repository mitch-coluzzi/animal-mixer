# Animal Mixer — Claude Code Spec

## Project overview

A browser-based animal mix-and-match game for kids. Players pick a base animal, then swap individual body parts (head, body, legs, tail) and stack multiple accessories on top. They can change the background scene, add a text label, and save their creation as a PNG to a shared Supabase gallery that all devices can browse.

Target users: kids ages 3–8, tablet-first, zero reading required for core interactions.

---

## Tech stack

- **Frontend:** Single-file vanilla HTML/CSS/JS (no framework, no build step)
- **Animal rendering:** Layered inline SVGs stacked absolutely inside a fixed canvas div
- **Photo capture:** `html2canvas` library → PNG blob
- **Backend:** FastAPI (existing Railway project)
- **Storage + gallery DB:** Supabase (existing project) — Storage bucket `animal-mixer` + table `animal_mixer_saves`
- **Hosting:** Served as a static file from the existing Railway FastAPI app at route `/mixer`

---

## File structure

```
/animal-mixer/
  index.html         ← entire game, single file
  /parts/
    /heads/
      tiger.svg
      elephant.svg
      monkey.svg
      frog.svg
      lion.svg
      deer.svg
    /bodies/
      tiger.svg
      elephant.svg
      bear.svg
      giraffe.svg
      panda.svg
    /legs/
      tiger.svg
      elephant.svg
      flamingo.svg
      frog.svg
      lion.svg
      duck.svg
    /tails/
      tiger.svg
      peacock.svg
      lion.svg
      fish.svg
      snake.svg
      horse.svg
    /accessories/
      party_hat.svg
      crown.svg
      bow_tie.svg
      glasses.svg
      bow.svg
      top_hat.svg
      elephant_trunk.svg
      frog_tongue.svg
      unicorn_horn.svg
      dragon_spikes.svg
      wings.svg
  /backgrounds/
    sky.svg
    jungle.svg
    desert.svg
    snowy.svg
    night.svg
    candy.svg
```

FastAPI adds one route:
```python
# main.py addition
from fastapi.staticfiles import StaticFiles
app.mount("/mixer", StaticFiles(directory="animal-mixer", html=True), name="mixer")
```

---

## SVG part system

### Coordinate system
Every part SVG uses `viewBox="0 0 400 500"`. The canvas div is `400×500px` (CSS, scales with container). All parts are positioned absolutely on top of each other with `width:100%; height:100%`.

### Layer render order (bottom to top)
1. Background (full bleed behind canvas)
2. Wings (behind body so they appear to sprout from back)
3. Body
4. Legs (overlaps body bottom)
5. Tail (overlaps body side/rear)
6. Head (overlaps body top)
7. Dragon spikes (runs along spine, on top of body/head)
8. All other accessories (hat, crown, horn, trunk, tongue, glasses, bow tie, bow, top hat)

### SVG art style requirements
- **Nick Jr. cartoony** — thick outlines (3–4px stroke), bold flat fills, no gradients, slightly wobbly/hand-drawn feel
- **Consistent palette per animal** — Tiger = `#E8823A` / `#D06A28`, Elephant = `#C8A87A` / `#A88A5A`, Frog = `#5DBB63` / `#3A9940`, Lion = `#E8A830` / `#C88010`, Bear = `#8B6914` / `#6B4A0A`, Giraffe = `#F5C858` / `#C8A020`, Panda = `#333` / `#fff`, Monkey = `#C8824A` / `#A86030`, Deer = `#F0D0A0` / `#C8A870`
- **Parts must align** — a head SVG's neck bottom should sit at approximately `y=420` in the 500-unit space; a body SVG's neck top at approximately `y=80`. This ensures heads from any animal seat naturally on any body.
- **Accessories anchor to head area** — hats/horns/crown anchor to approximately `y=60–100` (top of head). Trunk/tongue anchor to `y=260–300` (snout area). Bow tie anchors to `y=350–380` (neck/chest). Wings anchor to `y=180–220` (mid-body). Dragon spikes run `y=80` to `y=350` along the spine center.
- Generate each SVG file individually as clean, standalone `<svg viewBox="0 0 400 500">` with transparent background. No `<html>` wrapper.

### Selector tile thumbnails
Each part also needs a **40×40 thumbnail version** — same drawing, simplified/scaled to fit the tile. These are generated inline in the JS as data URIs or simply use the same SVG scaled down via CSS (`width:36px; height:36px; object-fit:contain`).

---

## UI layout

### Header bar
- Background: `#FF6B35`
- Left: "Animal **Mixer!**" logo — "Animal" white, "Mixer!" in `#FFE566`, font `Fredoka One` or `Arial Rounded MT Bold`
- Right: floppy disk icon button → opens save/gallery modal

### Main layout
Two columns, no scrolling on tablet landscape:
- **Left sidebar** `180px` wide — part selector panels
- **Right stage area** — fills remaining width

### Left sidebar — part selector
Five collapsible sections: Head, Body, Legs, Tail, Accessories.

Each section has:
- A section header row: icon (SVG shape, not emoji) + category name label (small, for Lillie/parents — non-readers navigate by pictures)
- A 3-column grid of picture tiles

**Tile design:**
- `52×52px`, `border-radius:12px`
- Default: `background:#FFF3E8`, `border: 2.5px solid #FFD4A8`
- Hover: scale up 1.06, border `#FF6B35`
- Active/selected: border `#FF6B35`, background `#FFE0CC`, outer glow `box-shadow: 0 0 0 2px #FF6B35`
- Contains the part's SVG scaled to `36×36px` centered
- **No text label needed** — image only (small name below is fine for Lillie but purely optional)

**Accessories section is multi-select** — tiles toggle on/off independently. All others are single-select (radio behavior within the category). Selected accessories show a checkmark badge (`position:absolute; top:2px; right:2px; width:14px; height:14px; background:#FF6B35; border-radius:50%; color:white; font-size:9px` with a ✓).

### Right stage area

**Top row — base animal picker:**
5 large round buttons (`64×64px`, `border-radius:16px`). Each shows a full-body mini animal SVG. Tapping one resets head + body + legs + tail to that animal, clears accessories. Active state: orange border + glow.

**Background selector:**
6 colored circle swatches (`28px` diameter). Active swatch gets an orange ring. Backgrounds:
- Sky: `#87CEEB` with sun + clouds SVG
- Jungle: `#4CAF50` with leaves SVG
- Desert: `#F4A460` with cactus SVG
- Snowy: `#B0C4DE` with snowflakes SVG
- Night: `#1A1A3E` with stars SVG
- Candy: `#FF8FAB` with swirls SVG

**Canvas:**
- `400×500px` display size (scale down on small screens with `transform: scale()`)
- `border-radius:20px`, border `3px solid #FFD700`
- Background SVG fills behind all layers
- All part SVGs stack absolutely, `position:absolute; top:0; left:0; width:100%; height:100%`
- Render order per layer stack above

**Text label area (below canvas):**
- A large tap-to-edit text field — `font-family: Fredoka One`, `font-size: 20px`, centered
- Default text: auto-generated combo name (see Combo Name logic)
- Tapping opens a big keyboard-friendly input overlay (full-width input, `font-size:24px`, bright border)
- Text renders inside a `background:#FFE566; border-radius:12px; padding:6px 20px` badge below the canvas
- This text is included in the PNG capture

**Action buttons (bottom):**
Three large round buttons with icon + small label:
- 🎲 **Mix!** (`background:#FFE566`) — randomizes all parts + background
- 💾 **Save** (`background:#FFB0C8`) — opens save/gallery modal
- 📷 **Photo** (`background:#B8F0C8`) — captures PNG, goes straight to save flow

---

## Combo name logic

Auto-generate a fun name from the selected parts. Logic:

```js
function getComboName(state) {
  const counts = {};
  ['head','body','legs','tail'].forEach(p => {
    counts[state[p]] = (counts[state[p]] || 0) + 1;
  });
  const animals = Object.keys(counts);
  if (animals.length === 1) return `Totally ${capitalize(animals[0])}!`;
  if (animals.length === 2) {
    const [a, b] = animals;
    return `The ${capitalize(a)}-${capitalize(b)}!`;
  }
  // 3+ animals — pick dominant + funniest combo
  const sorted = animals.sort((a,b) => counts[b]-counts[a]);
  return `The Wacky ${capitalize(sorted[0])}!`;
}
```

If accessories are applied, append a suffix:
- unicorn_horn → "...of Magic"
- dragon_spikes → "...of Fire"
- wings → "...Takes Flight"
- crown → "...Royale"
- party_hat → "...Party Animal"
- (default with any accessory) → "...Supreme"

Examples: "The Elephant-Tiger! of Magic", "Totally Tiger! Party Animal"

---

## Save / gallery flow

### Supabase setup

**Storage bucket:** `animal-mixer` (public read, authenticated write via anon key)

**Table: `animal_mixer_saves`**
```sql
create table animal_mixer_saves (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  image_url text not null,
  label text,
  combo_name text,
  state jsonb
);
```

`state` stores the full mix config for potential future "load" feature:
```json
{
  "base": "tiger",
  "head": "elephant",
  "body": "tiger",
  "legs": "flamingo",
  "tail": "peacock",
  "accessories": ["crown", "wings"],
  "background": "sky"
}
```

### Save flow (frontend)

1. User taps Save or Photo button
2. `html2canvas` captures the canvas div + label badge as PNG blob
3. **Label modal appears** (if not already named):
   - Large friendly input: "Give your animal a name!"
   - Big colorful keyboard-friendly text field
   - Two buttons: "Save it!" (primary, orange) and "Skip" (secondary)
   - Modal is a centered overlay, `border-radius:20px`, white background
4. Upload PNG to Supabase Storage: `animal-mixer/{uuid}.png`
5. Insert row to `animal_mixer_saves` with `image_url`, `label`, `combo_name`, `state`
6. Show **success animation**: big star burst, "Saved!" text, then transition to gallery

### Gallery view

Triggered by floppy disk icon in header OR after a successful save.

Full-screen overlay (or separate route `/mixer/gallery`):
- Header: "Our Creations!" + back arrow
- Grid: `repeat(auto-fill, minmax(160px, 1fr))` of saved images
- Each card: PNG thumbnail + label text below + date (friendly: "Today", "Yesterday", "3 days ago")
- Cards load from `animal_mixer_saves` ordered by `created_at desc`
- Tap a card → full-screen view of that image with label, close button
- No delete button (kids' gallery, keep it joyful — deletion is an admin/parent task)

Fetch from Supabase:
```js
const { data } = await supabase
  .from('animal_mixer_saves')
  .select('id, image_url, label, combo_name, created_at')
  .order('created_at', { ascending: false })
  .limit(50);
```

---

## Environment / config

The frontend needs two env values injected at build/serve time. Since this is a static file served from FastAPI, inject them via a template or a `/mixer/config.js` endpoint:

```js
// served by FastAPI at /mixer/config.js
window.SUPABASE_URL = "https://xxxx.supabase.co";
window.SUPABASE_ANON_KEY = "eyJ...";
```

FastAPI route:
```python
@app.get("/mixer/config.js")
def mixer_config():
    return Response(
        content=f'window.SUPABASE_URL="{os.getenv("SUPABASE_URL")}";window.SUPABASE_ANON_KEY="{os.getenv("SUPABASE_ANON_KEY")}";',
        media_type="application/javascript"
    )
```

`index.html` loads: `<script src="/mixer/config.js"></script>` before any app code.

---

## External libraries (CDN)

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
```

---

## Responsive / tablet behavior

- Target: iPad (768×1024) and similar Android tablets in landscape
- Canvas scales down with `transform: scale(0.75)` + `transform-origin: top center` on screens narrower than 600px
- Sidebar becomes a bottom sheet (horizontally scrollable row of category tabs) on portrait/phone — but tablet landscape is the primary target, don't over-engineer mobile
- Touch targets minimum `44×44px` everywhere

---

## Accessibility / kid-UX notes

- All interactive elements `cursor: pointer`
- Active/selected states must be visually obvious (thick orange border + glow)
- Tap feedback: all buttons do a quick `transform: scale(0.93)` on `:active`
- No hover-only states — everything works on touch
- Sound effects are a nice-to-have but out of scope for v1
- The gallery should auto-refresh after a save so the new creation appears immediately

---

## Out of scope for v1

- User accounts / login
- Deleting saves (parent admin task, handle via Supabase dashboard)
- Drag-and-drop part placement
- Animated animals
- Sound effects
- Sharing a link to a specific creation
