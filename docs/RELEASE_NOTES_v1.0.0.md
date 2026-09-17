# Codex Wisp v1.0.0

First complete Windows release of the Codex usage desktop pet.

## Highlights

- Approved idle character remains the default identity, with temporary typing, microphone and guitar/music poses.
- Stable priority: open usage panel → microphone → music → typing → idle.
- Automatically follows the active Codex desktop task through Windows accessibility; optional task pinning and task/project scope.
- Per-second local usage refresh and official account 5-hour/weekly quota reads with reset countdowns.
- Full nullable token accounting: official total, input, cache read/write, uncached input, output, reasoning, non-reasoning output, derived ratios and comparison view.
- Model, session, daily, today, 7-day, 30-day and local-recorded-lifetime breakdowns.
- CAD API-equivalent cost estimate using model/tier pricing and a dated Bank of Canada exchange rate.
- Local-only numeric telemetry parsing; no transcript export, model calls, keystroke content or audio recording.

## Verification

- 17 unit/UI tests cover nullable accounting, cache/reasoning subsets, resets, forks, duplicates, history, state priority/debounce, hover behavior, quota selection/countdowns and approved assets.
- Independent local JSONL reconciliation confirms session and model totals.
- Source and frozen builds were launched against the installed Codex client; the frozen build followed the active task and returned live quota data.
- Normal and 200% DPI views, all four poses, the compact panel and expanded analytics were visually inspected.

## Known limits

- Local recorded lifetime cannot include deleted or cloud-only records.
- Players must integrate with Windows System Media Transport Controls to trigger the music state.
- The code is MIT licensed; character artwork is excluded from that grant. See `docs/ARTWORK.md`.
