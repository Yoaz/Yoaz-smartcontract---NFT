// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    //For the token id
    uint256 public tokenCounter;

    constructor() public ERC721("Dogie", "Dog") {
        tokenCounter = 0; // initiate token counter to 0 upon deployment of contract
    }

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId); //inherited from openzeppelin, checks rather tokenId is free
        _setTokenURI(newTokenId, tokenURI); //setting current created token with its relevant token URI
        tokenCounter += 1; //increment our token Counter by 1
        return newTokenId;
    }
}
