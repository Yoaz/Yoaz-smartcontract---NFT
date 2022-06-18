from brownie import network, AdvancedCollectible, config
from scripts.helpful_scripts import get_account, get_contract, fund_with_link


def deploy_and_create_advanced():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    fund_with_link(advanced_collectible.address)
    collectible = advanced_collectible.createCollectible({"from": account})
    collectible.wait(1)
    print("New collectible was created!!")
    return advanced_collectible, collectible


def main():
    deploy_and_create_advanced()
