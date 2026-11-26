# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/alpha-working/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/alpha-working/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up the world's news of Wednesday 25 November 2026 in one image.

The v4 image carries 39 sourced stories with structured density:
13 numbered drawn cards (US tariffs on 14 partners, AI doubts sinking
chip stocks, the first foreign astronaut on Tiangong, ballistic
missiles on Kyiv, the Houthi Jeddah threat, the Gaza strike, the
Australia–Solomons treaty, Egypt's 31-dead fire, the Cartagena rescue,
the birthright-citizenship injunction, the Murmansk detention, Iraq's
border ruling, and the Nvidia probe), 26 numbered briefs, region and
field counts, a GMT day strip, a numbers strip, a pin map, and a
date-proof section that marks earlier-day near misses as not included.
V4 adds a high-contrast positive date-proof strip under the masthead
and raises card and brief legibility so the front page stays readable
at thumbnail size.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, under 1 MiB)
```

`main.py` is stdlib only and copies `entry.png` from this repository.
No network, deterministic: two runs write the same bytes. `entry.png`
was drawn locally by `build_v4.py` (Pillow, build tool only — not run
by the entrypoint) from the news brief in `NEWS_BRIEF.md`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=d397ay5y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
