# Ali Discogs project context

At the start of work, read [current context](docs/project/context.md) and
inspect `git status --short --branch`. Read the [backlog](docs/project/backlog.md)
when choosing work and [decisions](docs/project/decisions.md) when relevant.
Use `docs/project/` as the project-management source of truth.

After meaningful work, a decision, a discovered blocker, or an interruption,
update the relevant docs in the same turn:

- Keep `context.md` under about 100 lines: current state, active work, limitations,
  and one concrete next action. Move superseded handoffs into history.
- Keep actionable work in `backlog.md`, with stable IDs, status, and completion
  criteria. Distinguish suggested work from user-agreed priorities. Record
  completed work in history and remove it from the active backlog.
- Append concise dated milestones to `history.md`, including validation and
  material limitations. Record partial work honestly when interrupted.
- Record durable choices and rationale in `decisions.md`; label proposals until
  adopted. Put substantial implementation plans in `docs/plans/YYYY-MM-DD-topic.md`
  and link them from the relevant backlog entry.

Use Europe/Amsterdam dates. Treat saved counts and observations as dated
evidence; inspect current code, data, and Git before claiming current facts.
Do not invent test results or remote deployment/publication status. Keep setup,
commands, and architecture in README.md or technical docs rather than duplicating
them in project context.

Routine documentation upkeep is part of authorized work. A proposed backlog
item does not authorize implementation. Status or “what's next?” requests call
for a briefing and recommendation unless execution is also requested. These
instructions do not authorize automatic commits, pushes, or external changes.

When the user asks to use WhatsApp, use the native WhatsApp desktop app through
Computer Use by default.
