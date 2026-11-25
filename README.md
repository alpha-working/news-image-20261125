# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/alpha-working/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/alpha-working/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up the world's news of Wednesday 25 November 2026 in one image.

The image is a newspaper front page, "THE WORLD TODAY": Ukraine hits a Russian ship in the Gulf of Finland, the Houthis strike Riyadh's tallest tower, Indonesia's Vice-President resigns, Nvidia's all-hands after Huang's return, Israeli strikes in Gaza, NATO AWACS to Poland, the Sarkozy trial, the FBI database breach, Iraq seizing Kurdish oilfields, Iran's medicine and energy crisis, CrowdStrike buying Zscaler, and Malaysia returning Rohingya refugees — 35 stories in all.

## Run it

```sh
python3 main.py
# writes /output/entry.png (1024x1024 PNG, 156 KB)
```

`main.py` is stdlib only and copies `entry.png` from this repository. No network, deterministic: two runs write the same bytes. `entry.png` was drawn by `build_image.py` (Pillow, local build tool only — not run by the entrypoint) from the news brief in `NEWS_BRIEF.md`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=d397ay5y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
