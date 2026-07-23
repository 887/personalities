# Output styles

[Output styles](https://code.claude.com/docs/en/output-styles) are a separate
Claude Code mechanism from the skills in this repo. A skill is invoked
per-conversation (`/personalities:engineer`); an output style **replaces parts of
Claude Code's system prompt** for the whole session and is selected with
`/output-style`.

They overlap in intent, so this directory stashes the output-style form of the
registers that have one. Same discipline, different lever — pick whichever fits
how permanently you want it applied.

| File | Style name | Skill counterpart |
|---|---|---|
| [`concise-engineering.md`](concise-engineering.md) | Concise Engineering | [`skills/engineer`](../skills/engineer/SKILL.md) |

## Install

Claude Code reads output styles from `~/.claude/output-styles/` (user-level) or
`.claude/output-styles/` (project-level). Symlink so repo edits stay live:

```bash
mkdir -p ~/.claude/output-styles
ln -s "$PWD/output-styles/concise-engineering.md" ~/.claude/output-styles/concise-engineering.md
```

Then `/output-style` and pick **Concise Engineering**. `/output-style default`
returns to stock.
