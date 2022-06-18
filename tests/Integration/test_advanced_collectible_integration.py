from sqlite3 import adapt
from brownie import network
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_DEVELOPMENT
from scripts.AdvancedCollectible.deploy_advanced import deploy_and_create_advanced
import pytest
import time


def test_can_create_advanced_colletible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_DEVELOPMENT:
        pytest.skip("Only for testnet!!")
    # Act
    advanced_collectible, collectible = deploy_and_create_advanced()
    time.sleep(240)
    # Assert
    assert advanced_collectible.tokenCounter() > 0
