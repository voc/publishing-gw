import re
import time
import json
import requests
from os import environ
from urllib.parse import urljoin


VOCTOWEB_URL = "https://media.ccc.de"
# VOCTOWEB_URL = 'https://media.test.c3voc.de'
VOCTOWEB_API_KEY = environ.get("VOCTOWEB_API_KEY", "")

dry_run = True
slow_down = False

private_api = requests.Session()
private_api.headers.update(
    {
        "Content-Type": "application/json",
        "Authorization ": f"Token token={VOCTOWEB_API_KEY}",
    }
)

def graphql(query: str, **variables: dict):
    q = re.sub(r'\s+', '+', query)
    url = f"{VOCTOWEB_URL}/graphql?query={q}"
    if variables:
        url += "&variables=" + json.dumps(variables)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"  {response.status_code}\n" + response.text.split("\n")[0])
        if slow_down:
            time.sleep(5)
        return False

    body = response.json()
    if 'errors' in body:
        print(f"  {body['errors']}")

    return body["data"]

def get(uri):
    response = requests.get(urljoin(VOCTOWEB_URL, uri))
    if response.status_code != 200:
        print(f"  {response.status_code}\n" + response.text.split("\n")[0])
        return False
    return response.json()

def create_lecture_map(conference: str):
    # https://media.ccc.de/graphql?query={conference(id:%22camp2023%22){title,lectures{nodes{guid,slug}}}}
    query = '{conference(id:"' + conference + '"){title,lectures{nodes{guid,slug,video:videoPreferred{filename}}}}}'
    # {"conference":{"title":"Chaos Communication Camp 2023","lectures":{"nodes":[{"guid":"c793b7ba-e1e4-5a77-95e6-08ce4b4cb8ab","slug":"camp2023-57293-on_track_demoparty"},…
    lectures = graphql(query)["conference"]["lectures"]["nodes"]
    lookup_map = {}
    for talk in lectures:
        key = key_from_slug(talk["slug"])
        lookup_map[key] = talk
        alt_key = key_from_slug(talk["video"]["filename"], cleanup=True)
        if key != alt_key:
            lookup_map[alt_key] = talk

    return lookup_map


def key_from_slug(slug: str, cleanup=False):
    try:
        [conference, local_id, *rest] = slug.split("-")
        # if local_id is a number, we use camp2023-57136 as key
        if local_id.isdigit():
            return f"{conference}-{local_id}"
    except:
        pass
    # in all other cases we use the full slug as key
    if cleanup:
        return re.sub(r"(_[hs]d)?\.mp4$", "", slug)
    return slug


def upsert_recording(guid: str, data: dict):
    if not (dry_run):
        # create or update recording in voctoweb
        r = private_api.post(VOCTOWEB_URL + "/api/recordings", json={
            "guid": guid,
            "recording": {"folder": "", **data},
        })
        if r.status_code not in [200, 201]:
            print(f"  {r.status_code}\n" + r.text.split("\n")[0])
            if slow_down:
                time.sleep(5)
            if r.status_code == 422:
                return r.json()
            return False
        print(
            f"  {'created' if r.status_code == 201 else 'updated'} recording successfully"
        )
        print(f"    {r.text}")
        return r.json()
