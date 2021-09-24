import brownie


def test_wrap_erc721(owner, deployer, wrapXSet, testNFT):
    # Wrap, only owner and check properties
    wxs = wrapXSet()

    tokenId = 2
    testNFT.mint(owner, tokenId)

    testNFT.transferFrom(owner, wxs, tokenId, {"from": owner})
    wxs.setWrappedToken(testNFT, tokenId, {"from": owner})

    assert wxs.getWrappedAddress() == testNFT.address
    assert wxs.getWrappedTokenId() == tokenId

    assert wxs.name() == "wxs" + testNFT.name()
    assert wxs.symbol() == "wxs" + testNFT.symbol()
    assert wxs.tokenURI(tokenId) == testNFT.tokenURI(tokenId)
    assert wxs.tokenURI(tokenId + 1) == testNFT.tokenURI(tokenId)

    with brownie.reverts("NFTSet: caller is not owner nor approved"):
        wxs.setWrappedToken(testNFT, tokenId, {"from": deployer})


def test_wrap_not_erc721(owner, wrapXSet, testERC1155):
    wxs = wrapXSet()

    tokenId = 2
    testERC1155.mint(owner, tokenId, 1)

    testERC1155.safeTransferFrom(owner, wxs, tokenId, 1, "", {"from": owner})

    with brownie.reverts(""):
        wxs.setWrappedToken(testERC1155, tokenId, {"from": owner})


def test_wrap_erc721_not_owned(owner, wrapXSet, testNFT):
    wxs = wrapXSet()

    tokenId = 2
    testNFT.mint(owner, tokenId)

    with brownie.reverts(
        "WrapXSet: Wrapped token must be an ERC721 and owned by the contract"
    ):
        wxs.setWrappedToken(testNFT, tokenId, {"from": owner})


def test_not_wrapped_like_nftset(wrapXSet):
    # no wrap ~ nftset, check name/symbol
    name = "setName"
    symbol = "SNS"
    wxs = wrapXSet(name, symbol)

    assert wxs.name() == name
    assert wxs.symbol() == symbol


def test_unwrap(owner, wrapXSet, testNFT):
    # test properties after unwrap, setting to 0
    name = "setName"
    symbol = "SNS"
    wxs = wrapXSet(name, symbol)

    tokenId = 2
    testNFT.mint(owner, tokenId)

    testNFT.transferFrom(owner, wxs, tokenId, {"from": owner})
    wxs.setWrappedToken(testNFT, tokenId, {"from": owner})

    ZERO = "0x0000000000000000000000000000000000000000"
    wxs.setWrappedToken(ZERO, 0, {"from": owner})

    assert wxs.getWrappedAddress() == ZERO
    assert wxs.getWrappedTokenId() == 0

    assert wxs.name() == name
    assert wxs.symbol() == symbol


def test_withdraw(owner, deployer, wrapXSet, testNFT, TestNFT):
    # test withdraw no other token
    wxs = wrapXSet()

    tokenId = 2
    testNFT.mint(owner, tokenId)

    anotherNFT = TestNFT.deploy({"from": deployer})
    anotherId = 3
    anotherNFT.mint(owner, anotherId)

    testNFT.transferFrom(owner, wxs, tokenId, {"from": owner})
    wxs.setWrappedToken(testNFT, tokenId, {"from": owner})

    anotherNFT.transferFrom(owner, wxs, anotherId, {"from": owner})

    wxs.withdrawERC721(anotherNFT, anotherId, {"from": owner})
    assert anotherNFT.ownerOf(anotherId) == owner

    anotherNFT.transferFrom(owner, wxs, anotherId, {"from": owner})

    wxs.safeWithdrawERC721(anotherNFT, anotherId, {"from": owner})
    assert anotherNFT.ownerOf(anotherId) == owner

    anotherNFT.transferFrom(owner, wxs, anotherId, {"from": owner})

    with brownie.reverts("NFTSet: caller is not owner nor approved"):
        wxs.withdrawERC721(anotherNFT, anotherId, {"from": deployer})

    with brownie.reverts("NFTSet: caller is not owner nor approved"):
        wxs.safeWithdrawERC721(anotherNFT, anotherId, {"from": deployer})


def test_withdraw_wrapped(owner, wrapXSet, testNFT):
    # test cannot withdraw the wrapped, after reset ok
    # test withdraw no other token
    wxs = wrapXSet()

    tokenId = 2
    testNFT.mint(owner, tokenId)

    testNFT.transferFrom(owner, wxs, tokenId, {"from": owner})
    wxs.setWrappedToken(testNFT, tokenId, {"from": owner})

    with brownie.reverts("WrapXSet: Cannot withdraw the wrapped during its usage"):
        wxs.withdrawERC721(testNFT, tokenId, {"from": owner})

    ZERO = "0x0000000000000000000000000000000000000000"
    wxs.setWrappedToken(ZERO, 0, {"from": owner})

    wxs.withdrawERC721(testNFT, tokenId, {"from": owner})
    assert testNFT.ownerOf(tokenId) == owner
