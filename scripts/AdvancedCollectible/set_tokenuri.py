from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed


dog_metadata_dic = {
    "PUG": "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA-INU": "ipfs://QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST-BERNARD": "ipfs://QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"Working on network {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    for token_id in range(advanced_collectible.tokenCounter()):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    print(
        "Setting tokenURI for: {} in {} project".format(token_id, nft_contract.address)
    )
    print("TokenURI is set: {}".format(tokenURI))
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print("TokenURI is set for: {} in {}!!!".format(token_id, nft_contract.address))
    print("Please hit 'Refresh Metadata' and wait up to 20min to get it updated :)")
