# jeopardy-simplest-etl
- The simplest single-file python ETL pipeline, all contained in [etl.py](./etl.py).
- Scrapes information on the latest jeopardy games

# Components

## Extract
- Fetches the webpage with the list of episodes from the current season from [j-archive.com](https://www.j-archive.com/s)
- Saves as an html file.
## Transform
- Takes the episode list html file as its input
- Parse out game data from the webpage
- Saves transformed data in JSONL format
## Display
- Prints data to the console about the most recent games

# Usage
Call the `etl.py` script to execute all three steps.
```bash
python etl.py
```
**Sample output**
```
$ python etl.py

Game #8465 [Aired: 2021-08-13]
Description: Matt Amodio game 18. Last game of Season 37. Last...
Contestants:
  - Matt Amodio
  - Eric Shi
  - Nicolle Neulist

Game #8464 [Aired: 2021-08-12]
Description: Matt Amodio game 17. Champion's winnings & consolation amounts matched to KidSmart.
Contestants:
  - Matt Amodio
  - Steve Spillman
  - Ruth Reichard

...
```

# env file
This app reads a `.env` file with the following environment variables defined:
- CURRENT_SEASON: the current season written as an integer `37`. (defaults to `37` if no value supplied)
