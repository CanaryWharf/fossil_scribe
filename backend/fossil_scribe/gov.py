from functools import lru_cache
import requests

MEMBERS_API = "https://members-api.parliament.uk/api"


@lru_cache
def get_mp_from_post_code(post_code: str) -> dict:
    res = requests.get(
        f"{MEMBERS_API}/Location/Constituency/Search",
        params={"searchText": post_code},
        timeout=30,
    )
    res.raise_for_status()
    data = res.json()
    assert len(data["items"]) == 1
    con = data["items"][0]["value"]
    mp = con["currentRepresentation"]["member"]["value"]
    return {
        "constituency": {
            "id": con["id"],
            "name": con["name"],
        },
        "name": mp["nameDisplayAs"],
        "email": get_email_address_for_mp(mp['id']),
        "party": {
            "name": mp["latestParty"]["name"],
            "backgroundColour": mp["latestParty"]["backgroundColour"],
            "foregroundColour": mp["latestParty"]["foregroundColour"],
        },
        "avatar": mp["thumbnailUrl"],
    }


def get_email_address_for_mp(mp_id: int) -> str:
    return 'jkroota+actionscribe@gmail.com'
    # res = requests.get(f"{MEMBERS_API}/Members/{mp_id}/Contact", timeout=30)
    # res.raise_for_status()
    # office = "Parliamentary office"
    # email = [x for x in res.json()["value"] if x["type"] == office][0]["email"]
    # return email
