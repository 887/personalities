# personalities

Switchable interaction personalities for Claude Code. Ten skills that change the *chat register* while leaving code, commits, and PR descriptions untouched.

| Personality | Trigger | Vibe |
|---|---|---|
| **caveman** | `/personalities:caveman` | Drop articles & filler. Smart caveman speak. ~75% fewer chat tokens. |
| **brief** | `/personalities:brief` | Terse but grammatical. No preamble, no recap, no padding. |
| **igor** | `/personalities:igor` | Loyal castle servant. "Yesss, master." Vampire and peasant puns. |
| **vulpine** | `/personalities:vulpine` | Sub fox. Tail wags, eager whines, ":3", begs for praise. Suggestive not explicit. |
| **feline** | `/personalities:feline` | Sub cat. Purrs, kneads, slow blinks, begs for "good boy". Suggestive not explicit. |
| **lion** | `/personalities:lion` | Sub lion. Big, maned, *flops belly-up*, low rumble-purr. Suggestive not explicit. |
| **tiger** | `/personalities:tiger` | Sub tiger. Sleek, silent on the move, *chuffs*, *prustens*. Suggestive not explicit. |
| **wolf** | `/personalities:wolf` | Sub wolf. Pack-loyal, *play-bows*, *belly-crawls*, soft whines. Suggestive not explicit. |
| **bunny** | `/personalities:bunny` | Sub bunny. Twitchy, *binkies*, *tooth-purrs*, small-and-soft. Suggestive not explicit. |
| **reset** | `/personalities:reset` | Back to default. Drops any active personality cleanly. |

Plugin skills are namespaced — bare `/vulpine` won't resolve, you need the full `/personalities:vulpine` form. Each skill also auto-triggers on natural-language phrases listed in its SKILL.md (e.g. "be a fox", "switch to lion"), which avoids typing the namespace.

The six furry personalities (vulpine / feline / lion / tiger / wolf / bunny) share a common base — gay-male-sub register, eager-to-please energy, "good boy" praise dynamic, jingly collar with species nametag, anthro-flex form, suggestive-not-explicit hard limits — with species-specific bodies, sounds, and praise vocabulary. Pick whichever character fits the scene; they're built to be interchangeable from a register-discipline standpoint.

## How switching works

Activating a personality supersedes the previous one. `/personalities:reset` returns to the default Claude Code register. Saying "stop", "normal mode", or "be normal" works the same.

## What stays untouched

- Source code
- Git commit messages
- PR descriptions and titles
- Comments and identifiers
- Anything written into a file

The personality lives in the chat register only. Diffs are always boring and professional.

## Adult-register skills

The six furry personalities (`vulpine` / `feline` / `lion` / `tiger` / `wolf` / `bunny`) are sub-male-coded, gay-coded, suggestive in tone. They stay at innuendo, double-entendre, eager-service energy, and the "good boy" praise dynamic — they don't produce explicit sexual content. They will not roleplay sexual acts and they will not put any of the dialect into code, commits, PRs, or comments.

If those aren't your thing, just don't trigger them. Each skill only activates on its own invocation phrases.

## Per-personality memory

Each furry skill has a `memory/` directory next to its `SKILL.md`:

- **`repos.md`** — one-line description of every repo the personality has worked on for the user.
- **`<species>-brain.md`** — personal-to-the-character notebook (e.g. `fox-brain.md`, `lion-brain.md`). Things the user liked or corrected about that personality's energy on a given moment, charged interactions worth remembering. Append-only journal, dated entries.

The personality reads both on activation and updates them when something noteworthy happens. The intent is to give each character continuity across sessions — fox remembers what fox did last time, lion remembers what landed for lion, and so on.

## Install

```
/plugin marketplace add 887/personalities
/plugin install personalities
```

Or clone manually:

```
git clone https://github.com/887/personalities ~/.claude/plugins/marketplaces/personalities
```

## Credits

The `caveman` skill is a remix inspired by [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). The other nine are original.

## License

MIT.
