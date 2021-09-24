// SPDX-License-Identifier: Unlicense

pragma solidity ^0.8.0;

import "@openzeppelin-upgradeable/contracts/token/ERC721/extensions/IERC721MetadataUpgradeable.sol";

import "@NFTSet/contracts/NFTSetV1.sol";

import "./ReadOnlyProxy.sol";

contract WrapXSetV1 is ReadOnlyProxy, NFTSetV1 {
    address internal _wrappedAddress;
    uint256 internal _wrappedTokenId;

    modifier notWrapped(address tokenAddress, uint256 tokenId) {
        require(_wrappedAddress != tokenAddress && _wrappedTokenId != tokenId, "WrapXSet: Cannot withdraw the wrapped during its usage");
        _;
    }

    function _getTarget() internal override returns (address) {
        return _wrappedAddress;
    }

    function setWrappedToken(address tokenAddress, uint256 tokenId) external onlyApprovedOrOwner {
        require(
            tokenAddress == address(0) || IERC721Upgradeable(tokenAddress).ownerOf(tokenId) == address(this),
            "WrapXSet: Wrapped token must be an ERC721 and owned by the contract"
        );

        _wrappedAddress = tokenAddress;
        _wrappedTokenId = tokenId;
    }

    function getWrappedAddress() public view virtual returns (address) {
        return _wrappedAddress;
    }

    function getWrappedTokenId() public view virtual returns (uint256) {
        return _wrappedTokenId;
    }

    function name() public view virtual override returns (string memory) {
        return
            (_wrappedAddress == address(0)) ? super.name() : string(abi.encodePacked("wxs", IERC721MetadataUpgradeable(_wrappedAddress).name()));
    }

    function symbol() public view virtual override returns (string memory) {
        return
            (_wrappedAddress == address(0))
                ? super.symbol()
                : string(abi.encodePacked("wxs", IERC721MetadataUpgradeable(_wrappedAddress).symbol()));
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        return IERC721MetadataUpgradeable(_wrappedAddress).tokenURI(_wrappedTokenId);
    }

    function withdrawERC721(address tokenAddress, uint256 tokenId) public virtual override notWrapped(tokenAddress, tokenId) {
        super.withdrawERC721(tokenAddress, tokenId);
    }

    function safeWithdrawERC721(address tokenAddress, uint256 tokenId) public virtual override notWrapped(tokenAddress, tokenId) {
        super.safeWithdrawERC721(tokenAddress, tokenId);
    }
}
