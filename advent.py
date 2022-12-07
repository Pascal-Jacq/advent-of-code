#!/usr/bin/env python
import datetime
import json
from pathlib import Path

import extract
import requests
from IPython.display import display_html

URL = "https://adventofcode.com"


def ensure_data_path():
    data_path = Path("data")
    if not data_path.exists():
        data_path.mkdir()


ensure_data_path()


def load_cookies():
    filename = "session.json"
    try:
        cookies = json.load(open(filename))
    except FileNotFoundError:
        print(
            f"""\
{80*"-"}
Json file: {filename} not found
Connect to {URL}, login and retrieve your session cookie.
Then create the file {filename} and put your cookie in
It should look like : 
{{"session": "xxx"}}
{80*"-"}\
"""
        )
        raise
    return cookies


def get_today():
    return datetime.date.today().day


def get_year():
    return datetime.date.today().year


def display_leaderboard(leaderboard):
    owner_id = leaderboard["owner_id"]
    owner = leaderboard["members"][str(owner_id)]
    owner_name = owner['name'] or f'#{owner["id"]}'
    print(f"Leaderboard - {owner_name}")
    for idx, (stars, last_star, name) in enumerate(
        sorted(
            [
                (member["stars"], member['last_star_ts'], member['name'] or f'#{member["id"]}#')
                for member in leaderboard["members"].values()
            ],
            key=lambda x: (x[0], -x[1]),
            reverse=True,
        ),
        start=1,
    ):
        print(f"{idx:4d} - {stars:02d}* {name:30} @ {datetime.datetime.fromtimestamp(last_star)}")


class Advent:
    def __init__(self, day=None, year=2022):
        self.day = day or get_today()
        self.year = year
        self.cookies = load_cookies()
        self.base_url = f"{URL}/{year}"
        self.contents = {}

    @property
    def success(self):
        return "success" in self.contents

    @property
    def url(self):
        return f"{self.base_url}/day/{self.day}"

    @property
    def level(self):
        payload = self.contents["payload"]
        if "level" not in payload:
            return -1
        return int(payload["level"])

    def process_extract(self, page):
        if page.status_code != 200:
            raise RuntimeError(f"Error getting {page.url} : got status {page.status_code}")
        self.contents, self.extract = extract.extract_content(page)
        return self.contents

    def download_problem(self):
        self.page = requests.get(self.url, cookies=self.cookies)
        return self.process_extract(self.page)

    def pretty_display(self, idx=None):
        if "success" in self.contents:
            display_html(self.contents["success"], raw=True)
        content = self.contents["content"]
        key = idx or self.contents["position"]
        display_html(content[key], raw=True)

    def post(self, answer):
        payload = self.contents["payload"].copy()
        if self.level == -1:
            return {}
        payload["answer"] = answer
        self.page = requests.post(f"{self.url}/answer", cookies=self.cookies, data=payload)
        return self.process_extract(self.page)

    @property
    def input(self):
        input_name = f"data/{self.year:04}_{self.day:02}_input"
        file = Path(input_name)
        if not file.exists():
            page = requests.get(f"{self.url}/input", cookies=self.cookies)
            file.write_text(page.text)
        return file.read_text()

    def get_private_leaderboards(self):
        page = requests.get(f"{self.base_url}/leaderboard/private", cookies=self.cookies)
        root = extract.extract_html(page.text)
        private_boards = root.xpath('//article//a/@href')
        self.leaderboards = [requests.get(f"{URL}/{url}.json", cookies=self.cookies).json() for url in private_boards]
        return self.leaderboards

    def display_leaderboards(self):
        for leaderboard in self.get_private_leaderboards():
            display_leaderboard(leaderboard)
            print()

    def display_personal_stats(self):
        r = requests.get(f"{self.base_url}/leaderboard/self", cookies=self.cookies)
        root = extract.extract_html(r.text)
        stats = root.xpath('//article/pre')[0]
        print(stats.text_content())


def generate_notebook(day, year):
    notebook_file = Path(f"{year:04}_{day:02}_notebook.ipynb")
    if not notebook_file.exists():
        notebook = Path("template.ipynb").read_text()
        notebook = notebook.replace("api = Advent()", f"api = Advent(year={year}, day={day})")
        notebook_file.write_text(notebook)
    return notebook_file


if __name__ == "__main__":
    import os
    import sys

    try:
        day = int(sys.argv[1])
    except IndexError:
        day = get_today()
    try:
        year = int(sys.argv[2])
    except IndexError:
        year = get_year()
    print(f"Preparing notebook for day {day} (Year : {year})")
    notebook = generate_notebook(day, year)
    os.system(f"code {notebook} > /dev/null 2>&1 || echo 'Generated file {notebook}'")
