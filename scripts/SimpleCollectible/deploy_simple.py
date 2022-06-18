from scripts.helpful_scripts import get_account, sample_token_uri, OPENSEA_URL
from brownie import SimpleCollectible, config, network


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(f"Minted your NFT! ID # = {simple_collectible.tokenCounter() - 1}")
    print(
        f"You can now view your NFT at {OPENSEA_URL.format(simple_collectible.address,simple_collectible.tokenCounter() -1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()
