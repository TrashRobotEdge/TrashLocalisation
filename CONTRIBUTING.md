# How we work

**Flow:** board → pick an issue → assign yourself → Status *In Progress* → branch → PR → merge → Status *Done*.
- Board: https://github.com/orgs/TrashRobotEdge/projects/1. **Sprint** field = S0–S5 (S5 = final review & prep, 12–18/01), no sprint = backlog.
- Branch from `main`: `<issue-number>-short-name` (e.g. `12-hsv-detector`).
- Commits: [Conventional Commits](https://www.conventionalcommits.org), `type(scope): summary`, imperative, ≤72 chars, one change each (e.g. `feat(detector): publish edgetrash detections`). Types: `feat` `fix` `docs` `refactor` `test` `chore`.
- PR description: what + **why**, and `Closes #N`. Reviews are encouraged (big PRs: someone from the other course side), not mandatory.
- **Category** (board field): Setup · Build · Research · Decision (ends with an ADR) · Review prep (prepare a professor session) · Docs.
- **One issue ≈ 1 h, done in one sitting.** Bigger → split. **Max 2 per course per person per sprint** (+ an optional home issue). Doesn't fit → backlog.

**Every decision has a written "because".**
- Decision → ADR in `docs/decisions/` (copy `0000-template.md`, next number). Both repos number their ADRs from 0001: across repos, write "TL ADR 0001" / "ET ADR 0001".
- Something broke → `docs/problems.md`: symptom → diagnosis → alternatives (the professor grades this).
- Weekly → `docs/journal/sprint-N.md` (also our prep for the professor's review).

**Never commit:** model files (`.pt .onnx .tflite .hef .blob`), datasets, rosbags, `build/ install/ log/`, Windows `Zone.Identifier` files.
Big files go to GitHub Releases (or the shared drive) with a checksum and a download script.

**Docs as you go:** docstrings in code, a paragraph in `docs/` when a piece works. The reports are assembled from these, not written from memory at the end.
