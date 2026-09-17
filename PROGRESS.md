# Project Progress

Status: IN PROGRESS

## Current Objective
Finish and publish Codex Wisp: preserve approved idle character/UI, add only typing, microphone and music activity states, transient hover/click usage panel, complete token analytics, Windows executable and GitHub release.

## Completed
- Isolated repository cloned; personal website untouched. GitHub upload permission verified; current repo visibility private.
- Live Qt panel with original ice-spirit icon, task-following via Windows accessibility document title, manual pinning, task/project scope, total/input/output, context, 5h/weekly quotas, CAD estimate, tray, compact mode, drag/keyboard movement.
- Hidden official Codex app-server quota RPC works every second. No model calls or widget credential reads.
- Incremental JSONL usage reading and read-only SQLite metadata work. Five initial unit tests pass; live window screenshot verified.
- Persistent AGENTS.md and this recovery file added following the user attachment.
- Nullable raw/derived analytics, model/session/calendar-day history, raw field detail and reset countdowns implemented. Eleven unit tests pass. Live expanded smoke succeeds with quota data and correct active task.
- Approved transparent Skirk-style character integrated in `pet.py`, original asset `assets/skirk-pet.png` MUST NOT be changed. User approved existing idle UI and only requested temporary activity variations.
- Three transparent activity sprite edits generated from the approved original; the original idle asset is byte-for-byte unchanged.
- `activity.py` detects only keyboard timing, microphone capture-session activity, and Windows media playback state. Stable debounce and the approved panel > microphone > music > typing > idle priority are implemented.
- Hover/click usage reveal and automatic leave-to-pet behavior are implemented without activating the widget window or stealing keyboard focus.
- Fork aggregation now removes inherited ancestor snapshots while retaining each child session's unique work. Local raw-record reconciliation succeeds.
- Final README, token-accounting reference, artwork notice, MIT code license, third-party notices and reproducible PyInstaller build script added.
- Visual QA found and fixed a white Qt scroll viewport that made the main panel hard to read.
- Frozen startup failure diagnosed to Codex runtime PATH contaminating PyInstaller dependency discovery with a versioned ICU 78 DLL. The build now filters that path and standardizes the compatible PySide VC runtime.

## Files Modified
AGENTS.md, PROGRESS.md, DESIGN.md, docs/implementation-plan.md, usage.py, analytics.py, analytics_view.py, desktop.py, widget.py, pet.py, activity.py, assets/, tests/, tools/, requirements*.txt, .gitignore.

## Important Decisions
- Source: local Codex `state_*.sqlite` + JSONL sessions; UIA document LegacyIAccessible Name follows actual active task. Initial URL is stale and must never select the task.
- App-server only initializes and reads account/rateLimits/read; exact 300 and 10080 minute windows selected. Public Bank of Canada USD/CAD daily series.
- Token source total includes cached input and reasoning output. Enhancement must replace missing-as-zero behavior with explicit unknown coverage without removing fields.
- Default pet toggles the existing panel; analytics in a separate modeless details window. Preserve all quota functionality and add visible reset countdowns.
- Upload is already authorized; do not change repo visibility. All screenshots with live personal data stay ignored in `.private/`.
- Activity priority: transient usage panel > microphone > music > typing > idle. Detect only activity booleans/timestamps, never typed text or audio content. Hide usage after leaving pet/panel, respecting open settings/details.
- Reference: https://github.com/ccusage/ccusage (MIT; active). Studied cumulative/last-request parsing and cache subset normalization; no code copied, kept Python architecture. https://store.steampowered.com/app/3419430/Bongo_Cat/ inspires temporary key-reactive posing only, not replacement character art.

## Current State
Source app and enhanced analytics run; all 17 tests pass. A clean Windows onedir build and zip succeed, and the corrected frozen executable follows the active task with live quota and activity-detector data. No new commit/release yet. Staging review and GitHub delivery are the active stage.

## Known Issues
- No GitHub commit/release or desktop shortcut yet.
- Media playback detection depends on Windows System Media Transport Controls, so players that do not integrate with Windows media controls cannot be detected reliably.
- Microphone detection reports active Windows capture sessions; the app never opens or records the microphone.
- The release executable is not code-signed; Windows may show its normal unknown-publisher/SmartScreen prompt on another machine.

## Tests / Verification
- 17 unit/UI tests pass: price/cache math, nullable accounting, dedup/partial lines/resets/forks/model changes, calendar aggregation, state priority/debounce, transparent assets, hover reveal, N/A cache writes, countdown preservation, task matching and quota duration/expiry.
- Approved idle asset SHA-256 remains `7ce0d2fbd0eb89d2f6786c9bb1d5bada1aff7d89ea2f5dd079cce8a26483e1a0`; every activity sprite has a real transparent alpha channel.
- Independent local raw-record reconciliation: 28 sessions reconciled; model and session sums match; warm cached read about 0.005 seconds.
- Official quota RPC, UIA title and public FX verified live.
- `.private/first.png` shows live panel; title followed a switch to the 3D website task correctly.
- Normal and 200% DPI synthetic views inspected: all four poses, compact panel and analytics are legible without clipping.
- Clean frozen `CodexWisp.exe --smoke` exits 0, follows `构建沉浸式3D个人网站`, reads usage and gets live account quota. The release tree contains no foreign ICU copied from the Codex tool runtime.
- Final frozen smoke follows `开发实时用量悬浮 Widget`, reports live quota, `keyboard_hook_error: null`, and valid microphone/music booleans. A synthetic F24 key event triggered the real low-level hook and selected `typing` without capturing text.
- Final archive: 53,316,751 bytes; SHA-256 `339598CC41F9D15A7B778A0C2CF6B73513CB0BF6C4918B7704216B7FCCE4E26E`.
- Source/private-data scan found no credential signatures or personal absolute paths; `.private/`, build output, dist output, virtualenv and generated spec are ignored.

## Remaining Work
1. Stage only reviewed source/assets/docs, run staged diff/secret checks, commit and push main.
2. Publish authorized private GitHub release v1.0.0 with the verified Windows zip.
3. Create a desktop shortcut, launch the finished app, verify process is running, then mark this file COMPLETE and push the final state.

## Next Step
Stage the reviewed source set, inspect the cached diff, commit and push main, then publish release v1.0.0.
