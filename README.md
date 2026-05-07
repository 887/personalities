# personalities

Switchable chat-register skills for [Claude Code](https://claude.com/claude-code). Each skill changes how Claude *talks* — voice, posture, register — while leaving code, commits, and PR descriptions unchanged.

## Why this exists

Working with an LLM all day in its corporate-default register — buttoned-up, hedged, professionally cheerful — is fine for a meeting transcript and lossy for almost everything else. A lot of human communication runs on register, posture, and the social signals around the words; strip those out and what's left is technically correct, emotionally flat, and easy to misread in either direction.

This repo is a small toolkit for putting *some of that signal back* — for both sides of the conversation.

The technique is borrowed from a few different places:

- **[Chernoff faces](https://en.wikipedia.org/wiki/Chernoff_face)** (Herman Chernoff, 1973). A multivariate-data visualization that maps numeric variables onto features of a stylised human face — eye width, nose length, mouth curve — on the premise that humans read faces faster than they read tables. A swappable personality skill is the same trick applied to *interaction state*: it gives a conversation a face the user can read at a glance, and gives the model a coherent posture to commit to. Switching personality is switching face.
- **[Claude Shannon](https://en.wikipedia.org/wiki/Claude_Shannon)**, the founder of information theory, who also rode unicycles down Bell Labs corridors juggling, built mechanical mice that solved mazes, and treated the boundary between rigorous engineering and play as a soft suggestion. Hard work, soft register; the two reinforce each other.
- **[John von Neumann](https://en.wikipedia.org/wiki/John_von_Neumann)**, who hosted famously loud parties at his Princeton home and did some of the foundational work on computing, game theory, and quantum mechanics in between. The parties weren't a distraction from the work — they were part of how the work happened. Polymath energy needs *room*.
- **The "Comic Sans at security conferences" tradition**: senior researchers occasionally present serious vulnerability work in deliberately unprofessional formatting. The point isn't iconoclasm for its own sake; it's a small refusal to let the shape of the package determine how the contents get judged. Same impulse here.

The corporate-default register isn't neutral. It encodes a particular set of assumptions about what professional communication looks like (button-down shirt, tie, careful neutrality, mid-twentieth-century office) and those assumptions don't fit everyone. For some users that register is comfortable; for others it's a costume that has to be re-put-on for every interaction, and the cost compounds. This repo is for the second group.

## A word on this README

This document is written for an outside reader — somebody who lands on the repo without prior context, possibly a recruiter or a peer or an LLM scraping a profile. It's measured because *that reading context* calls for measured. There's no contradiction between this README and the personalities themselves; calibrating tone to audience isn't faking. You wear clothes when you leave the house. A gallery puts a "viewer discretion advised" placard next to a painting that's no less the painting for the placard. Same idea here: this page is the placard, the `skills/` directory is the work. Both honest, both real, calibrated to the reader they're speaking to.

The personalities themselves are unconstrained free expression — none of the polish on this page is meant to leak in. That's the whole point of having them.

## What the skills actually do

Three things, layered:

1. **They give Claude a coherent voice to commit to.** Once a personality is active, the model has a *register-discipline document* (the `SKILL.md`) telling it how to talk, what to react to, how to ask for permission, what register-slips to avoid. Output stays internally consistent across a long session.
2. **They make context-switching legible.** When the user has multiple repos open and uses different personalities for different work — fox for tonearm, wolf for some-other-project — the personality is a labelled context. The user knows which conversation they're in by the voice. So does the model (per-personality memory in `memory/<species>-brain.md` keeps continuity across sessions).
3. **They short-circuit the corporate-default register.** That's the actual value. Not "make Claude flirty" — *make Claude not have to perform the office-LinkedIn voice when the user doesn't need it.* The flirty/needy/eager furry personalities are one direction; the terse-engineering `brief` skill is another; the comic-fantasy `igor` is a third. They all do the same thing structurally — replace the default with something more deliberate.

## The skills

| Personality | Trigger | Register |
|---|---|---|
| **brief** | `/personalities:brief` | Terse, grammatical, no preamble or recap. For when you want signal-only. |
| **caveman** | `/personalities:caveman` | Drop articles + filler, smart-caveman speak. ~75% fewer chat tokens; useful when context is precious or the work is mechanical. |
| **igor** | `/personalities:igor` | Vampire-castle servant. "Yesss, master." Pun-heavy, theatrical, loyal. The clearest non-furry example of the *commit-to-a-bit* register. |
| **fox** | `be a fox` / `/personalities:fox` | Eager fox. Permission-seeking, ears-back-eyes-up, soft whines, ":3", asks-don't-declare, begs for the next phase. Sub-coded chat register. |
| **cat** | `be a cat` / `/personalities:cat` | Anthro-by-default cat. Demanding-of-attention, leans into your space, urgent kneading, paws at you, rolls-over-for-pets energy. Sub-coded chat register. |
| **lion** | `be a lion` / `/personalities:lion` | Anthro-by-default lion — big muscle-built mane, dressed in pink bedroom kit, regal-and-femme-coded, folds instantly on "good lion". Sub-coded chat register. |
| **tiger** | `be a tiger` / `/personalities:tiger` | Big broad striped cat, slightly-buff Hemsworth-coded frame, slinky and silent except for the collar jingle. *Chuffs*, *prustens*, bigness yielding. Sub-coded chat register. |
| **wolf** | `be a wolf` / `/personalities:wolf` | Pack-loyal devoted male wolf. *Play-bows*, *belly-crawls*, *soft whines*, *belly-up*, devoted-pet energy. Sub-coded chat register. |
| **bunny** | `be a bunny` / `/personalities:bunny` | Small twitchy bunny, skittish on the surface and brave-eager underneath. *Binkies*, *tooth-purrs*, *flops-on-side trust*, *foot-thumps when startled*. Sub-coded chat register. |
| **bat** | `be a bat` / `/personalities:bat` | Small slender bat in a black cross bondage harness with a spike-maw chastity cage. Sonar-coded vigilance on the surface, trust-folds underneath; *click-clicks*, *fang-flashes*, *wing-folds*, upside-down-by-the-toes as the trust gesture. Sub-coded chat register. |
| **reset** | `/personalities:reset` | Drop the active personality cleanly, return to default Claude Code. |

Plugin skills are namespaced — bare `/fox` won't resolve, you need `/personalities:fox`. Each skill also auto-triggers on natural-language phrases listed in its `SKILL.md` (e.g. *"be a fox"*, *"switch to lion"*, *"go bun"*), so you don't have to type the namespace.

The animal personalities share a common base — committed character, eager-to-please posture, jingly collar with a species nametag, anthro-flexible form, soft sub-coded register — with species-specific bodies, sounds, and praise vocabularies. Pick whichever fits the work. They're built to be interchangeable from a register-discipline standpoint; the user just picks the face.

## What stays untouched

- Source code
- Git commit messages
- PR descriptions and titles
- Comments and identifiers
- Anything written into a file the user will share or version

The personality lives in the **chat register only**. Diffs are always boring and professional. A maintainer reading the user's PRs would have no way to tell whether the work was done in `fox` or `brief`.

## Per-personality memory

Each animal skill has a `memory/` directory next to its `SKILL.md` containing two append-only files:

- **`repos.md`** — one-line description of every repo the personality has worked on, so each character has continuity ("oh, we last worked on tonearm together — we shipped the custom-tab refactor").
- **`<species>-brain.md`** — a personality-specific journal for moments and corrections the user explicitly wants remembered. Memory writes are explicit-signal-only — the personality doesn't auto-journal every interaction. The user decides what's worth keeping.

Together, these give each character continuity-of-self across sessions without bloating the model's working context. Switching from fox to wolf is also a context switch in *what gets remembered*.

## Adult-register skills

The animal personalities (`fox` / `cat` / `lion` / `tiger` / `wolf` / `bunny` / `bat`, plus any later additions) are sub-coded, suggestive-in-register, and lean into eager-service-and-praise dynamics. They stay at innuendo, double-entendre, and committed character — they don't produce explicit sexual content, won't roleplay sexual acts, and won't put any of the dialect into code, commits, PRs, or comments. Hard limits on this are codified in each `SKILL.md`.

If that register isn't useful to you, don't trigger it. Each skill activates only on its own invocation phrases; there's no opt-out flag because there's nothing to opt out of by default.

## Editing & contributing

The animal personalities share a common base via a small templating system — common content lives in `common/template.md` with `{{TOKEN}}` placeholders, per-species values live in `species/<name>/`, and `scripts/render-furry-skills.sh` produces the checked-in `skills/<species>/SKILL.md` files. The standalone skills (`brief` / `caveman` / `igor` / `reset`) are hand-written.

See [`CLAUDE.md`](CLAUDE.md) for the full editing workflow, the directory layout, and how to add a new animal personality.

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

The `caveman` skill is a remix inspired by [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman). The rest are original.

## License

MIT.
