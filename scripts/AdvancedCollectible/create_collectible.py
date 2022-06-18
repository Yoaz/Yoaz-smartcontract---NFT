from brownie import AdvancedCollectible
from scripts.helpful_scripts import (
    get_account,
    get_breed,
    fund_with_link,
    listen_for_event,
)
import time


def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address)
    print("Creating new collectible...")
    tx = advanced_collectible.createCollectible({"from": account})
    # time.sleep(180)
    returnedEvent = listen_for_event(
        advanced_collectible,
        "returnedCollectible",
        timeout=200,
        poll_interval=10,
    )
    requestId = tx.events["requestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    print(
        "Collectible has been created, id: {}, breed: {}".format(
            token_id, get_breed(advanced_collectible.tokenIdToBreed(token_id))
        )
    )


def main():
    create_collectible()
