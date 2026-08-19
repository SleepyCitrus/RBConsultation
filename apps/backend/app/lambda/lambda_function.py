import json
import os
import requests

from riftbound import COMMON, ORIGINS, RIFTBOUND, get_card_slug, get_staple_cards_dict

GAMES_URL = "https://api.justtcg.com/v1/games"
CARDS_URL = "https://api.justtcg.com/v1/cards"

def get_game_slugs():
    response = requests.get(
        GAMES_URL,
        headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]},
    )

    response.raise_for_status()

    for game in response.json()["data"]:
        if game["id"].contains("riftbound"):
            print(game["id"], game["name"])

def get_card():
    """
    Test function to get a single card. 
    If getting multiple cards, use get_cards() instead.
    """
    
    response = requests.get(
        CARDS_URL,
        headers={"x-api-key": os.environ["JUSTTCG_API_KEY"]},
        params={
            "game": RIFTBOUND,
            # "cardId": get_card_slug("defy", ORIGINS, COMMON),
            "tcgplayerId": "652814",
            "condition": "NM",
            "printing": "Normal",
            "priceHistoryDuration": "1y",
        },
    )
    response.raise_for_status()
    if response.json():
        print(response.json())

def get_cards():
    all_staples = get_staple_cards_dict()
    json_list = []
    for slug, staple in all_staples.items():
        temp = {
            "game": RIFTBOUND,
            "tcgplayerId": staple.tcgplayer_id,
            "condition": "NM",
            "printing": staple.printing,
            "priceHistoryDuration": "1y",
        }
        json_list.append(temp)

    chunks = [json_list[i:i + 20] for i in range(0, len(json_list), 20)]
    for chunk in chunks:
        response = requests.post(
            CARDS_URL,
            headers={
                "x-api-key": os.environ["JUSTTCG_API_KEY"], 
                "Content-Type": "application/json"
            },
            json=chunk
        )

        response.raise_for_status()
        if response.json():
            print(response.json())


def lambda_handler(event, context):

    # get_game_slugs()
    # get_card()
    get_cards()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }