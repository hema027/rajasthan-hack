# CloneTrace Memory & Working Context

## Current Step

- Completed: Analyst console (SOC/abuse-desk design), prototype rule-based scorer, `--corpus` pipeline, ReportLab takedown PDF dossiers, pure-Python replay resolver.
- Ready for mentoring demo and Step 3 model training / APK analysis.
- Step 2 complete. Tag: v1.2-fix.
Stub scorer reads labels.label for synthetic observations. This makes
confusion matrix, campaign sizes, and ARI trivially 1.0. This is intended
for plumbing only. Step 3 replaces the stub with a real feature-based model;
after Step 3 the numbers become honest (expected ~0.9-0.95 precision/recall).

## What Works (verified)

- `detect/fetcher.py`: Pure-Python offline resolver (`resolve()`) over `data/sites/<host>/manifest.json` with Playwright file-based screenshot capture (`capture_screenshots()`), fast benchmark, and zero external network calls.
- `detect/model.py`: Prototype rule-based heuristic scorer using `config.yaml` weights (`password_or_pin_input`, `cross_origin_form_action`, `unauthorized_brand_domain`, `lure_keywords`, `punycode_or_homoglyph`, `risky_tld`, `exfil_endpoint`). Marked `# TODO(step3): replaced by the trained model`.
- `pipeline.py`: Supports `--corpus` mode (runs on 190 synthetic corpus observations, finds 8 distinct campaigns) and default `seed` mode (runs on 41 seed observations, finds 5 campaigns with $ARI = 1.0$).
- `graph/build.py` & `graph/cluster.py`: Graph construction and Louvain clustering support optional `obs_ids` filtering to cleanly segregate seed vs corpus campaign computations.
- `report/takedown.py`: Standardized abuse escalation PDF dossier (< 6 pages, black on white with `#4C8DFF` accent headers, evidence table, side-by-side screenshots, shared infrastructure, and unresolved recipient status).
- `app/streamlit_app.py` & `app/theme.py`: SOC analyst work surface console (Triage, Campaigns, Intake, Report, Metrics) with Linear/Splunk dark theme (`#0F1115`), monospace tokens, and no emojis/gradients.
- `tests/`: 21 tests passing in full test suite (`test_smoke.py`, `test_fetcher.py`, `test_ingest.py`, `test_corpus.py`).

## What Is Stubbed / TODO

- `detect/features.py`: `# TODO(step 2): real implementation` (deep DOM tree parsing, visual/OCR models).
- `detect/model.py`: `# TODO(step3): replaced by the trained model` (ML classification model & ensemble scoring replacing heuristic prototype).
- `detect/apk.py`: `# TODO(step 3): real implementation` (static APK parsing via androguard/androzero).
- `graph/enrich.py`: `# TODO(step 2): real implementation` (live WHOIS, RDAP, passive DNS queries).

## Key Decisions & Why

- **Pure-Python Resolver**: Removed route interception and local replay HTTP servers to eliminate socket/Chromium hangs on Windows. Playwright is retained exclusively for offline `file://` screenshot rendering.
- **Data Segregation**: `obs_ids` filter in `build_graph` and `cluster` separates synthetic corpus campaigns from seed benchmark campaigns in the SQLite database.
- **Analyst Console UX**: Employs an internal SOC/abuse-desk aesthetic (Splunk/Grafana/Linear) avoiding generic landing-page cards, rounded badges, or emojis.

## Known Gotchas

- **Streamlit sys.path**: Running `streamlit run app/streamlit_app.py` sets script directory to `app/`. Explicit `sys.path.insert(0, repo_root)` and try/except fallback imports ensure module resolution without extra package files.
- **PyVis CDN Resources**: Headless Streamlit components require `cdn_resources="remote"` on pyvis `Network` to load vis-network JS from CDN rather than broken relative local file paths.
- Never present the current 1.0 precision/recall to judges. It is a lookup
  table, not a model.
- The graph builder filters on verdicts.label. Do not change this. In Step 3
  the verdicts will be real predictions, and the graph will reflect them.

## Contract Changes

- **2026-10-07**: Added `prototype_scorer` configuration block to `config.yaml` with documented entry in `CHANGELOG.md`.

## Next Actions

- [ ] Present analyst console during mentoring round (Triage, Campaigns, Intake live pivot, Report PDF).
- [ ] Step 3: Implement trained ML classifier in `detect/model.py`.
- [ ] Step 3: Static APK parsing in `detect/apk.py`.

## Session Log

- **2026-10-07T17:34:00+05:30**: Implemented Phase A (prototype rule-based scorer in `detect/model.py`, `pipeline.py --corpus`), Phase B (SOC Analyst Console in `app/streamlit_app.py`, `app/theme.py`, `.streamlit/config.toml`), and Phase C (ReportLab takedown PDF in `report/takedown.py`). All 21 tests green.
