from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_DEVELOPMENT, get_contract
from scripts.AdvancedCollectible.deploy_advanced import deploy_and_create_advanced
import pytest


def test_can_create_advanced_collectible():
    # Deploy contract
    # Create an NFT
    # Get a random breed
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip(
            "Only for local testnig!"
        )  # Unit test are for locl development networks only
    # Act
    advanced_collectible, collectible = deploy_and_create_advanced()
    requestId = collectible.events["requestedCollectible"]["requestId"]
    RANDOM_NUMBER = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, RANDOM_NUMBER, advanced_collectible.address
    )
    # Assert
    assert advanced_collectible.tokenCounter() > 0
    assert (
        advanced_collectible.tokenIdToBreed(advanced_collectible.tokenCounter())
        == RANDOM_NUMBER % 3
    )
