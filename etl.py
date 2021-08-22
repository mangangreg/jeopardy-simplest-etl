import re
import os
import json
import unicodedata

import dotenv
import requests
import pandas as pd

dotenv.load_dotenv('.env')
CURRENT_SEASON = os.environ.get('CURRENT_SEASON', 37)
BASE_URL = "https://www.j-archive.com"
RE_LINK_CELL = r"#(?P<game_no>\d+), aired (?P<air_date>[0-9\-]+)"
NL='\n'

def extract():
    ''' Grab the episode list for current season '''
    # Query the current season
    response = requests.get(f"{BASE_URL}/showseason.php", params={'season': CURRENT_SEASON})
    # Write to file
    with open(f"season_{CURRENT_SEASON}.html", 'w') as wfile:
        wfile.write( response.text )

def transform():
    ''' Transform step: parse html and conver to JSONL'''
    df_in = pd.read_html(f"season_{CURRENT_SEASON}.html")[0]
    df_in.columns = ['ep', 'contestants', 'description']
    df_in.ep = df_in.ep.apply(lambda x: unicodedata.normalize("NFKD", x).strip())

    df_out = df_in.ep.str.extract(RE_LINK_CELL)
    df_out['contestants'] = df_in.contestants.apply(lambda s: [x.strip() for x in s.split('vs.')])
    df_out['description'] = df_in.description

    df_out.to_json(f"season_{CURRENT_SEASON}.jsonl", orient='records', lines=True)

def load():
    ''' Load step: Just print formatted data to console '''
    data = [json.loads(row) for row in open(f"season_{CURRENT_SEASON}.jsonl").readlines()]
    for row in data[:5]:
        print(f"\nGame #{row['game_no']} [Aired: {row['air_date']}]\nDescription: {row['description']}")
        print(f"Contestants:\n{NL.join('  - '+x for x in row['contestants'])}")

def main():
    extract()
    transform()
    load()

if __name__ == '__main__':
    main()