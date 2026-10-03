# PSLE Cheat Sheets — Claude context

A small Flask site of exam-prep cheat sheets built for one family's PSLE
(Singapore Primary 6 Leaving Exam) revision — currently Math and Science,
plus a countdown review plan. Not affiliated with MOE/SEAB.

## Scope & purpose

- **Scope**: every topic, question, and worked example on this site is
  Singapore **Primary 5** syllabus. The PSLE itself is sat at the end of
  P6, but the son is currently in P5, so all content should track what
  he's being taught and examined on *now* — P5, not P6. P6-scoped content
  doesn't belong here (the old Map Maths category was P6 and was removed
  for exactly this reason — see History below). When in doubt about
  whether something is P5 or P6 syllabus, check before adding it.
  "P5 syllabus" is interpreted as what the son is actually being taught
  and tested on at the P5 level — including assessment-book/enrichment
  material his worksheets use — not strictly the official MOE syllabus
  document. For example, parallelogram and trapezium area formulas
  aren't officially named in the MOE P5 (or even P6) syllabus — the
  official approach is to split those shapes into rectangles/triangles —
  but they were added to the Area topic anyway at the user's explicit
  request, since they matched what the son's materials cover. Confirm
  the P5/P6 boundary, surface it if content looks like it's really P6 or
  beyond, but don't block on "is this the official syllabus" alone.
- **P4 exception**: on 2026-10-03 the user asked for a Primary 4 Science
  cheat sheet built from a photo of the P4 textbook contents page, so
  there is now a separate `/science-p4` page (`templates/science_p4.html`,
  blue accent, chapters 1–7). It is last year's revision material and is
  deliberately kept on its own page so the main Math/Science pages stay
  P5-only. Don't mix P4 content into the P5 pages; link between them
  instead. Apart from the P4 and P3 pages, P6 content still doesn't
  belong here unless the user asks for it.
- **P3 exception**: on 2026-10-03 the user also asked for a Primary 3
  Science cheat sheet from a photo of the P3 textbook contents page:
  `/science-p3` (`templates/science_p3.html`, plum accent, chapters 1–7:
  living/non-living, classification, materials, plant and animal life
  cycles, magnets). Same rule as P4: its own page, linked from the others.
- **Purpose**: this is a living cheat sheet, not a one-off Q&A log. When a
  Primary 5 exam question or a piece of relevant syllabus information
  comes up in conversation — the user asks about a topic, shares a
  question from a worksheet or paper, or it surfaces while researching —
  the default is to capture it into the appropriate cheat-sheet page (a
  new topic section, a new worked example, or an addition to an existing
  rule/example), not just answer it in chat and leave it there. Treat
  "explain X" or "give me examples of Y" as an implicit "...and add it to
  the cheat sheet," following the Content workflow below, unless the user
  is clearly just asking a quick one-off question about something already
  on the page (e.g. "what does this rule mean?").

## Structure

- `app.py` — Flask app. Routes: `/` (index), `/math`, `/science`,
  `/science-p4`, `/science-p3`, `/plan`,
  each just `render_template`-ing the matching file in `templates/`.
- `templates/index.html`, `math.html`, `science.html`,
  `science_p4.html`, `science_p3.html`, `plan.html` — one
  self-contained HTML file per page (styles inline in `<style>`, no shared
  CSS/JS files, no JS at all beyond `<details>` disclosure widgets).
- `dev_server.py` — run this instead of `app.py` while editing; wraps the
  app with `livereload` so template/app-code changes refresh the browser
  automatically. Needs `requirements-dev.txt` installed (not part of the
  production deploy).
- `requirements.txt` / `requirements-dev.txt` — prod is just
  `Flask` + `gunicorn`; dev adds `livereload` on top via `-r requirements.txt`.
- `render.yaml` — deploys to Render as a free-tier web service:
  `pip install -r requirements.txt` then `gunicorn app:app`.

## Running locally

- Prod-style: `python app.py` (Flask debug server) or `gunicorn app:app`.
- With live-reload: `python dev_server.py` → http://127.0.0.1:5001, watches
  `templates/*.html` and `app.py`.
- `app.config["TEMPLATES_AUTO_RELOAD"] = True` is already set in `app.py`,
  so Jinja template edits show up on refresh even without `dev_server.py`.
- Both `app.py` and `dev_server.py` run on port **5001**, not Flask's
  default 5000 — on most Macs, port 5000 is claimed by the system's
  AirPlay Receiver, and hitting `http://127.0.0.1:5000` lands on that
  instead of the app, showing a confusing "Access to 127.0.0.1 was
  denied" in the browser rather than connecting to Flask.

## Design system (shared conventions across every page)

- Fonts: "Bricolage Grotesque" (display/headings) + "Lexend" (body), both
  via Google Fonts `<link>` tags.
- Theming via CSS custom properties on `:root`: `--bg`, `--surface`,
  `--ink`, `--muted`, `--line`, `--accent`, `--on-accent`, `--tint`,
  `--formula`, `--warn-bg`/`--warn-ink`/`--warn-line`, `--shadow`,
  `--display`, `--body`, `--mono`.
- Dark mode is set twice, deliberately: once under
  `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ... } }`
  for OS-level dark mode, and once under `:root[data-theme="dark"] { ... }`
  for an explicit in-page toggle (if one is ever added). Keep both in sync.
- Each page has its own accent color (e.g. Math is violet `#6A3FA0`
  /`#B79AF0` dark; Science and Plan have their own). `--accent` drives
  links, pills, the `.ans` answer tags, SVG strokes, etc., so changing one
  variable re-themes the whole page.
- Shared component classes reused across pages: `.panel`, `.rules`,
  `.steps`, `.ans`, `.warn`, `details.try` (collapsible "try it yourself"),
  `.figs`/`figcaption`, `.scroll`/`table` (horizontally-scrollable data
  tables), `.checklist`, `.sitebar` (cross-page nav breadcrumb), `.nav`
  (sticky in-page topic pills), `.sec`/`.sec-head` (topic sections).
- Inline SVG diagram helper classes: `.shape` (tint fill + accent stroke),
  `.plain` (surface fill + accent stroke), `.dash` (dashed muted line),
  `.ray` (solid ink line), `.arc` (accent stroke arc), `.sq` (small
  right-angle marker), `.lbl` (bold label text), `.mut` (muted small text).
- `.cat-switch`/`.cat-pill` exist in the CSS history for pages that offer
  more than one syllabus-level category to switch between (a `--cat-color`
  custom property per pill). Not currently used on any page — Math used to
  have a P6/P5 switcher but P6 was removed (see History below) — but the
  pattern is there if a page needs it again.

## Content workflow (adding or editing a topic section)

1. Confirm the content is genuinely Primary 5 syllabus (not P6) before
   writing anything — the site's scope is P5 only (see Scope & purpose
   above). A web search is worth doing when the P5/P6 boundary on a topic
   isn't obvious.
2. Draft the rules list + 2–3 worked examples.
3. Verify every worked-example calculation with Python (`fractions.Fraction`
   for exact arithmetic) before it goes in the HTML — do not hand-check PSLE
   maths.
4. Build the section HTML reusing the shared classes above; add new SVG
   helper classes only if an existing one doesn't fit.
5. Smoke-test with the Flask test client:
   `app.test_client().get("/math")` etc. — check status 200 and a sane
   response length.
6. Run a local dev server and screenshot the new section(s) with Playwright
   (`/opt/pw-browsers/chromium`), at both a desktop width and a mobile
   width (~390px), to catch layout/overflow/text-clipping bugs before
   shipping. Use `page.locator("#id").scroll_into_view_if_needed()` then
   `page.screenshot()` per section.
   - Avoid port 5060 for the dev server — it's on Chromium's blocked
     "unsafe ports" list and Playwright navigation to it will fail. Use
     something like 8000–8003 instead.
   - If an SVG label near the edge gets clipped, widen the `viewBox`
     rather than shrinking the font or anchor-hacking it.
7. Sync + commit (see Environment notes below), then rebuild/redeliver the
   zip if the user wants a fresh download.

## Environment notes for whoever (whichever Claude session) is editing this

- This repo may be edited from two different places: a sandboxed cloud
  workspace copy, and the user's real Mac
  (`~/Documents/PSLE/psle-site`) reached through a device bridge. They are
  **separate filesystems** — always be clear about which one a given
  command is touching.
- The Mac's Python `venv` (`venv/bin/python3`) is a symlink into an
  Anaconda install on the Mac and does **not** resolve from inside the
  sandboxed cloud shell — don't try to `pip install` into it from there.
  Either have the user run installs themselves in their own Terminal, or
  (for genuinely dev-only tooling) keep it in `requirements-dev.txt`.
- The cloud sandbox generally **cannot `git push`** to GitHub — SSH host
  key verification fails there. Commits can be made locally in either
  environment, but pushing to `origin` needs to happen from the user's own
  Terminal: `cd ~/Documents/PSLE/psle-site && git push origin main`.
- The device bridge to the Mac can silently disconnect/reconnect mid-task.
  **After syncing a file to the Mac, verify it actually landed** (e.g.
  `grep`/`diff` against the source of truth) rather than trusting a
  success response alone — a sync once failed mid-transfer and left the
  Mac's `math.html` stale for a user-visible gap until it was caught via a
  bug report.
- Git remote: `origin = git@github.com:jicheng17/PSLE.git`, branch `main`.

## History / notable decisions

- The Math page originally covered P6 "Map Maths" (geography-flavoured
  maths: scale, journeys/speed, weather data, land/water area, compass
  turns) with a P5 Math category added alongside it behind a two-pill
  category switcher, each category visually scoped to its own accent color
  via a `.p5-scope`-style class.
- On 2026-10-01 the P6 Map Maths category was removed entirely at the
  user's request, along with the category switcher. The Math page is now
  P5 Math only (Angles, Area, Volume, Fractions, Decimals, Rate,
  Percentage, Exam habits), and its root `:root` palette was promoted to
  the violet accent that P5 content used to get via scoping.
- The P5 Science page follows the textbook chapter numbers and titles
  (Ch 1 Reproduction in Animals and Plants, Ch 2 Cycles in Water, Ch 4
  Human Respiratory and Circulatory Systems, Ch 5 Electrical Systems).
  Not yet written up: Ch 3 Plant Transport System and Ch 6 parallel
  circuits. The Ch 4 "Humans vs fish" section is an extension that isn't
  in the textbook contents; the textbook's own blood-flow chart is the
  nine-step flow chart in the circulatory section.
- On 2026-10-03 `science_p4.html` was added (P4 chapters: Plant System,
  Human Systems, Matter, Light, Shadows, Heat, Effects of Heat). The last
  topic of Ch 7 was cut off in the contents photo, and the Ch 2 overview
  of body systems (skeletal/muscular rows) is a best guess — check against
  the textbook if the user reports gaps.
- On 2026-10-03 `science_p3.html` was added (P3 chapters: Diversity of
  Living and Non-living Things, Classification of Living Things,
  Diversity of Materials, Life Cycles of Plants, Life Cycles of Animals,
  Properties of Magnets, Making and Using Magnets). The facts were written
  at P3 level from the textbook's topic questions only (the pages
  themselves weren't seen), so the classification groups (flowering /
  non-flowering plants, with / without a backbone, fungi, bacteria) and
  the list of animal life cycles are best guesses — check against the
  textbook if the user reports gaps. The home page card grid now uses
  `auto-fit` columns so more cards can be added.
