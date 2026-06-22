# Project Context Protocol

The master package stays universal. Project-specific files live outside the master docs.

For each active build project, keep a separate project folder containing:

- a project lessons/context file (e.g. `MASTER_LESSONS_LEARNED.md`) — design target, constraints, active decisions, screenshot- or user-approved baselines, and project-only lessons and validated preferences
- the active build script for that project
- `studies/` — isolated studies, never mixed into the baseline until promoted

Universal lessons discovered inside a project should be promoted into the master `/rules` folder immediately, so the master package accumulates reusable knowledge while project specifics stay in the project folder.
