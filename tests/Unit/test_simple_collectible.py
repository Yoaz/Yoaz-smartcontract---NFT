from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_DEVELOPMENT
from scripts.SimpleCollectible.deploy_simple import deploy_and_create
from brownie import network, SimpleCollectible
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip()
    simple_collectible = deploy_and_create()
    assert (
        simple_collectible.ownerOf(simple_collectible.tokenCounter() - 1)
        == get_account()
    )
