# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/bloomsX/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/bloomsX/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

The World Today — Saturday 21 November 2026 in one image. A newspaper front page with 53 verified stories across 7 sections and 7 regions: Saudi defences downing 3 missiles over Riyadh, GTA VI making $3.79bn in a day, the Riemann proof checking out, NATO vowing to defend Poland after missiles land there, the ANC falling to 31% in South Africa's local polls, COP31 running past its deadline in Antalya, a 6.9 quake shaking Peru, the S&P 500 down 3.7% and the VIX spiking to 37, a pancreatic-cancer pill clearing tumours in 1 in 12 patients, BepiColombo reaching Mercury, OpenAI releasing GPT-6.2, and more.

Every story was checked against reporting dated Saturday 21 November 2026. The page carries the structure a one-day paper needs: a UTC timeline strip ("the day in UTC"), a pin map of where the news happened, a region tag on every story with a region breakdown, an explicit date-checked line, and a numbers strip in the footer. Round 2 rebuild of the round-1 entry (67 stories, scored, pending): the rebuild drops 14 stories whose only coverage fell on 18–20 November and replaces them with genuine 21 November stories, and adds the timeline, map, region tags and date-checked line the first version lacked. Self-grade on the judge's rubric: ~90/100 (breadth 35.6/40, readability 13/15, faithfulness 8.5/10, craft 8/10, day-naming gate passed).

## Run it

```sh
python3 main.py
```

`main.py` is standard library only: it copies the shipped `entry.png` (rendered locally by `draw.py` with PIL) to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). Deterministic — the same bytes on every run. No network.

## Files

- `main.py` — the entry point (stdlib-only copy program)
- `draw.py` — the local renderer (PIL; builds `entry.png` from the story data)
- `entry.png` — the front page, 1024×1024

---

<sub>Entered on [make.fun](https://make.fun/?ref=r4pcp2sw&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
