#!/usr/bin/env python
import requests
import base64
from argparse import ArgumentParser


argp = ArgumentParser(prog="spotybpm")
argp.add_argument("query", metavar="QUERY")
argp.add_argument("key", metavar="KEY")
args = argp.parse_args()

key = args.key
q = args.query

auth = base64.b64encode(
    '8224cd2f0f2045a5a9c31b0f299c4886:5f46db7c276244a89d95dcc5f94105b6'.encode('ascii')
)

a = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {auth.decode('ascii')}"},
    data={"grant_type": "client_credentials"}
).json()


def strip(url):
    return url.replace("https://api.spotify.com/v1/", "")


def query(url, access):
    if "https" in url:
        url = strip(url)
    return requests.get(
        f"https://api.spotify.com/v1/{url}",
        headers={"Authorization": f"Bearer {access['access_token']}"}
    ).json()


results = query(f"search?type=track&q={q}", a)

possible = []

for r in results["tracks"]["items"]:
    if q.lower() in r["name"].lower():
        possible.append({
            "name": r["name"],
            "artists": [i["name"] for i in r["album"]["artists"]],
            "id": r["id"]
        })
for n, i in enumerate(possible[:10]):
    print(f"[{n}] {i['name']}\t({', '.join(i['artists'])})")

while True:
    try:
        sel = input("\nSelect track: ")
        if sel == "":
            sel = 0
            break
        else:
            sel = int(sel)
            break
    except ValueError:
        pass


stats = query(f"audio-features/{possible[sel]['id']}", a)

if key == "bpm":
    key = "tempo"

if (s := stats.get(key)) is not None:
    print(f"output: {s}")



