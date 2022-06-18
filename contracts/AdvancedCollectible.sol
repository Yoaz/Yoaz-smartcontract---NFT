// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BRENAND
    }
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomResult;
    uint256 public tokenCounter;
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;
    mapping(address => uint256) addressToTokenAmount;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);
    event returnedCollectible(bytes32 indexed requestId, uint256 randomNumber);

    constructor(
        address _vrfCoordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) public VRFConsumerBase(_vrfCoordinator, _link) ERC721("Dogie", "DOG") {
        tokenCounter = 0;
        fee = _fee;
        keyHash = _keyHash;
    }

    function createCollectible() public {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender; // Since fulfilRandomness is called by the VRFCoordinator
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        require(randomness > 0, "Random not found!");
        Breed breed = Breed(randomness % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        _safeMint(requestIdToSender[requestId], newTokenId); // Checks rather current token ID is available
        requestIdToTokenId[requestId] = newTokenId;
        tokenCounter += 1;
        emit returnedCollectible(requestId, randomness);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // Pug, Shiba-Inu, St-Bernanrd
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
