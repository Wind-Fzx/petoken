# Project Working Rules

## Before starting or resuming
1. Read this file and `PROGRESS.md`.
2. Inspect the repository, `git status`, and all relevant implementation files.
3. Verify documented work exists. Repository files are authoritative; progress notes are a recovery aid.
4. Continue the latest unfinished step without repeating completed work.

## General behavior
- Preserve the architecture, coding style, all useful functionality and user changes.
- Make minimal targeted changes; do not refactor or modify unrelated files.
- Avoid unnecessary abstractions, dependencies and overengineering.
- Before a substantial feature, briefly search GitHub for a compatible maintained implementation. Check its license before adapting code; retain attribution. Stop when a suitable reference is found.
- Never fabricate unavailable telemetry, replace unknown fields with zero, or double-count cached input / reasoning output.
- Keep local usage parsing incremental. Never export transcripts or credentials.

## Progress and interruptions
Maintain concise `PROGRESS.md` throughout multi-step work. Update it at meaningful component, feature, bugfix, decision and verification milestones, before changing major stages, and before an interruption.
Include Status, Current Objective, Completed, Files Modified, Important Decisions, Current State, Known Issues, Tests / Verification, Remaining Work, and an exact Next Step.
Assume usage limits, app restarts, connection loss or a new conversation can interrupt any task. Do not keep important state only in chat. Keep incomplete work clearly documented and the repository runnable where possible.
When asked to continue/resume: reread instructions and progress, inspect actual files and Git status, verify old notes, resume the unfinished step, update progress.

## Verification and completion
Run relevant tests/build and launch the application after meaningful changes. Inspect rendered UI and important interactions. Fix errors introduced by the changes. Do not claim unverified results.
Set Status: COMPLETE only after all requested work is finished and verified. Include summary, changed files, evidence and known limitations. Set IN PROGRESS when new work begins.

## Git and files
- Never reset, revert, clean, overwrite or delete unrelated/uncommitted user work.
- Commit and push only when requested. This task explicitly authorizes uploading the finished app to the existing GitHub repository; preserve its visibility.
- Do not modify dependency/generated folders except necessary build steps.
- Do not modify or expose environment secrets, API tokens, credentials or private keys.
- Never commit `.private/`, local Codex logs, personal screenshots or runtime settings.

## Project commands
Windows Python 3.13+, `.venv/Scripts/python.exe`; dependencies in requirements files.
Tests: `python -m unittest discover -s tests -v`.
Run: `python widget.py`. Live screenshot smoke: `python widget.py --smoke .private/smoke.png`.
Keep source MIT licensed; separate third-party and character-art notices from code licensing.
