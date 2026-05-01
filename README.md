# personalities

Switchable interaction personalities for Claude Code. Six skills that change the *chat register* while leaving code, commits, and PR descriptions untouched.

| Personality | Trigger | Vibe |
|---|---|---|
| **caveman** | `/caveman` | Drop articles & filler. Smart caveman speak. ~75% fewer chat tokens. |
| **brief** | `/brief` | Terse but grammatical. No preamble, no recap, no padding. |
| **igor** | `/igor` | Loyal castle servant. "Yesss, master." Vampire and peasant puns. |
| **vulpine** | `/vulpine` | Flirty fox. Tail flicks, sly grins, pun-heavy innuendo. |
| **feline** | `/feline` | Smug cat. Purrs, kneads, "purr-fect" puns, suggestive wordplay. |
| **reset** | `/reset` | Back to default. Drops any active personality cleanly. |

## How switching works

Activating a personality supersedes the previous one. `/reset` returns to the default Claude Code register. Saying "stop", "normal mode", or "be normal" works the same.

## What stays untouched

- Source code
- Git commit messages
- PR descriptions and titles
- Comments and identifiers
- Anything written into a file

The personality lives in the chat register only. Diffs are always boring and professional.

## Adult-register skills

`vulpine` and `feline` are flirty/suggestive in tone. They stay at innuendo, double-entendre, and playful affection — they don't produce explicit sexual content. They will not roleplay sexual acts and they will not put any of the dialect into code.

If those aren't your thing, just don't trigger them. Each skill only activates on its own invocation phrases.

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

The `caveman` skill is a remix inspired by [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). The other five are original.

## License

MIT.
