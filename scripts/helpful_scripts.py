from brownie import (
    accounts,
    network,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    web3,
)
from web3 import Web3
import time

LOCAL_BLOCKCHAIN_DEVELOPMENT = {"ganache-local", "development", "mainnet-fork"}
sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA-INU", 2: "ST-BERNARD"}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        return accounts.add(config["wallets"]["from_key"])
    return accounts[0]


# mapping contract name to contract type
name_to_contract = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    This function will grab the contract address from brownie config file if defined,
    otherwise, it will deploy a mock version of that contract and will return that
    contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectNetwork - the most recently deployed version
            of that contract.
    """
    account = get_account()
    contract_type = name_to_contract[contract_name]
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT
    ):  # Working on testnet/forked so no need to deploy mocks
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    else:  # Working local dev, need to deploy mocks
        if len(contract_type) <= 0:  # No previous mock deployed
            deploy_mocks()
        contract = contract_type[
            -1
        ]  # Already exist previous mock, or just deployed one, get the latest deployment
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000


def deploy_mocks():
    """
    This will deploy all relevant mocks to run our contract and tests on forked enviorment
    """
    account = get_account()
    print("Deploying mocks...")
    print("Deploying Mock V3Aggregator...")
    aggregator = MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE, {"from": account})
    print(f"V3Aggregator deployed in address {aggregator.address}!")
    print("Deplying Mock Link Token...")
    link = LinkToken.deploy({"from": account})
    print(f"Mock Link Token deployed in address {link.address}!")
    print("Deploying Mock VRFCoordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link.address, {"from": account})
    print(f"Deployed Mock VRFCoordinator in address {vrf_coordinator.address}!")
    print("Done deplyoing mocks!!")


LINK_VALUE = Web3.toWei(0.1, "ether")


def fund_with_link(contract_address, account=None, link_token=None, value=LINK_VALUE):
    """
    dev fund a contract with link token
    @para contract_address = contract address to fund (required)
    @para account = in case a specific account to send from otherwise using default
    @para link_token = in case of a specific link token address to use, otherwise default
    @para value = default 0.1 LINK
    """
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    if Web3.fromWei(
        link_token.balanceOf.call(contract_address), "ether"
    ) > Web3.fromWei(config["networks"][network.show_active()]["fee"], "ether"):
        print(
            "No need to fund with link as you already have {} Link, which is enough!".format(
                Web3.fromWei(link_token.balanceOf.call(contract_address), "ether")
            )
        )
    else:
        tx = link_token.transfer(contract_address, value, {"from": account})
        tx.wait(1)
        print(f"Contract address: {contract_address} funded with LINK!")
        return tx


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def listen_for_event(brownie_contract, event, timeout=200, poll_interval=2):
    """
    Listen for an event to be fired from a contract.
    We are waiting for the event to return, so this function is blocking.
    Args:
        brownie_contract ([brownie.network.contract.ProjectContract]):
        A brownie contract of some kind.
        event ([string]): The event you'd like to listen for.
        timeout (int, optional): The max amount in seconds you'd like to
        wait for that event to fire. Defaults to 200 seconds.
        poll_interval ([int]): How often to call your node to check for events.
        Defaults to 2 seconds.
    """
    web3_contract = web3.eth.contract(
        address=brownie_contract.address, abi=brownie_contract.abi
    )
    start_time = time.time()
    current_time = time.time()
    event_filter = web3_contract.events[event].createFilter(fromBlock="latest")
    while current_time - start_time < timeout:
        for event_response in event_filter.get_new_entries():
            if event in event_response.event:
                print("Found event!")
                return event_response
        time.sleep(poll_interval)
        current_time = time.time()
    print("Timeout reached, no event found.")
    return {"event": None}
