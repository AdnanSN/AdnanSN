# How the profile is printed

The profile README is a stack of "printouts" on green-bar paper. Everything here is plain Python 3 with no packages.

| File | What it does |
| --- | --- |
| `build_static.py` | Builds `assets/header.svg`, `exhibit.svg`, `journey.svg` and `footer.svg`. All the wording lives at the top of each section. |
| `stats.py` | Prints `stats.svg` (activity and languages). The nightly workflow runs it. |
| `printshop.py` | Shared paper, type and chart drawing. |
| `glyphs.json` | Letter shapes, so the images look the same on every computer. |
| `extract_glyphs.py` | Rebuilds `glyphs.json` from the font files (needs `fonttools`). You only need it to add new characters. |

## Change the words

1. Edit the text in `build_static.py`, for example a new line in `LOG` or a new commit at the top of `COMMITS`.
2. Run `python3 .github/readme/build_static.py` from the repository root.
3. Commit the updated files in `assets/`.

Lines are 80 characters wide. The script stops and names the line if something would run off the paper.

## The nightly sheet and the snake

`.github/workflows/profile-graphs.yml` runs every night, and whenever these files change. It publishes `stats.svg`, `snake.svg` and `snake-dark.svg` to the `output` branch, which the README reads from. To print a fresh copy straight away, open **Actions → Profile graphs → Run workflow**.

To include private repositories in the language bar, add a personal access token as a repository secret and pass it to the stats step in place of `GITHUB_TOKEN`. Repository names are never printed.

Fonts: IBM Plex Mono, Doto and Caveat, all under the SIL Open Font License (see `OFL.txt`).
