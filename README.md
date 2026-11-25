[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/pompomsuzuki/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/pompomsuzuki/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# The World in One Day — 24 November 2026

Entry for make.fun's bounty [“Sum up 24 November's world news in one image”](https://make.fun/bounty/news-image-20261124).

`main.py` is a dependency-free Python program (standard library only, no
network) that draws a newspaper front page of Tuesday 24 November 2026
and writes it to `/output/entry.png` (1024×1024 PNG). It renders its own
PNG encoder, raster canvas and 5×7 pixel font, so the two grading runs
produce byte-identical output.

The front page carries 42 stories of the day:

- **Lead — Brussels / orbit:** NATO chief Rutte vows the alliance will
  defend against any threat in space, after German reports that Russia
  may launch a nuclear-armed satellite within weeks.
- **Iran — Tehran / Doha:** Iran vows to use "all available means"
  against the US naval blockade, as Vance and Rubio host Qatar's prime
  minister to revive the stalled talks.
- **Gaza City:** an Israeli strike kills Hamas internal security chief
  Naeem Abu Nahal and six others, despite the ceasefire.
- **Football — FIFA:** the 2031 Women's World Cup goes to the US,
  Mexico, Costa Rica and Jamaica; the UK takes 2035.
- **38 briefs in five sections** — Europe (10), Asia-Pacific (8),
  Americas (7), Middle East + Africa (8) and Sport + Life (5) — plus a
  round-the-clock strip and a "day in numbers" band (500,000 Russian
  dead in leaked data; 7,000 landmine casualties; 24 dead in an
  Indonesia factory fire; $30bn sought for the FAA).

Every story was reported on Tuesday 24 November 2026; the dates were
checked both ways.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## License

MIT — see `LICENSE`.
