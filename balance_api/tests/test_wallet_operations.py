import pytest
from balance_api.wallet_operations import create_wallet, get_balance
from eth_tester import EthereumTester
from web3 import EthereumTesterProvider, Web3


@pytest.fixture(scope="module")
def tester():
    return EthereumTester()


@pytest.fixture(scope="module")
def mock_web3():
    w3 = Web3(EthereumTesterProvider())
    return w3


def test_create_wallet_variation(mock_web3):
    return (
        create_wallet(w3=mock_web3)["public_key"]
        != create_wallet(w3=mock_web3)["public_key"]
    )


def test_get_balance(mock_web3, tester):
    accounts = tester.get_accounts()
    for account in accounts:
        account_balance = Web3.from_wei(tester.get_balance(account), "ether")
        assert (
            get_balance(account, "ether", w3=mock_web3).get("balance")
            == account_balance
        )


@pytest.mark.skip(reason="For the future send_transaction...")
def test_send_transaction(mock_web3, tester):
    addr1, addr2 = tester.get_accounts()[:2]
    hash_tr = tester.send_transaction(
        {
            "from": addr1,
            "to": addr2,
            "gas": 30000,
            "value": 5,
            "max_fee_per_gas": 1000000000,
            "max_priority_fee_per_gas": 1000000000,
            "chain_id": 131277322940537,
        }
    )
    assert hash_tr
