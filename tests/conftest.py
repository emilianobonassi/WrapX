import pytest

from brownie import config


@pytest.fixture
def deployer(accounts):
    yield accounts[0]


@pytest.fixture
def owner(accounts):
    yield accounts[1]


@pytest.fixture
def TestNFT(pm):
    yield pm(config["dependencies"][2]).TestNFT


@pytest.fixture
def testNFT(deployer, TestNFT):
    yield TestNFT.deploy({"from": deployer})


@pytest.fixture
def testERC1155(pm, deployer):
    TestERC1155 = pm(config["dependencies"][2]).TestERC1155
    yield TestERC1155.deploy({"from": deployer})


@pytest.fixture
def wrapXSetV1Logic(deployer, WrapXSetV1):
    yield WrapXSetV1.deploy({"from": deployer})


@pytest.fixture
def nftSetFactory(pm, deployer, wrapXSetV1Logic):
    NFTSetFactory = pm(config["dependencies"][2]).NFTSetFactory
    yield NFTSetFactory.deploy(wrapXSetV1Logic, {"from": deployer})


@pytest.fixture
def wrapXSet(owner, nftSetFactory, WrapXSetV1):
    def l(name="A", symbol="BBB"):
        tx = nftSetFactory.create(name, symbol, {"from": owner})
        return WrapXSetV1.at(tx.events["ProxyCreated"]["proxy"])

    yield l
