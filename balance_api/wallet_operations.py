import logging
import os

from web3 import Web3
from web3.exceptions import InvalidAddress

logger = logging.getLogger(__name__)
CURRENCY_CONVERT = {"eth": "ether"}


web3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER", "")))


def create_wallet(w3: Web3 = web3) -> dict[str, str]:
    """Creating an account in the blockchain"""
    acct = w3.eth.account.create()
    address = acct.address
    private_key = w3.to_hex(acct._private_key)
    logger.info(f"Generated PUB: {address} adn PRIV: {private_key}")
    return {"public_key": address, "private_key": private_key}


def get_balance(
    address: str, currency: str, w3: Web3 = web3
) -> dict[str, float | str | None]:
    """Getting a balance in the specified currencies"""
    try:
        balance = w3.eth.get_balance(address)
    except InvalidAddress as e:
        return {"balance": -1, "error": str(e.args[0])}
    return {
        "balance": Web3.from_wei(balance, CURRENCY_CONVERT.get(currency, "ether")),
        "error": None,
    }


# NOT TESTED!!!
def send_transaction(
    from_address: str,
    to_address: str,
    amount: float,
    currency: str,
    private_key: str,
    w3: Web3 = web3,
) -> dict[str, str | None]:
    """Transfer of currency to another address"""
    value_wei = int(Web3.to_wei(amount, CURRENCY_CONVERT.get(currency, "ether")))
    gas_price = w3.eth.gas_price
    gas = 2_000_000
    nonce = w3.eth.get_transaction_count(from_address)
    transaction = {
        "chainId": web3.eth.chain_id,
        "from": from_address,
        "to": to_address,
        "value": value_wei,
        "nonce": nonce,
        "gasPrice": gas_price,
        "gas": gas,
    }

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    except ValueError as ve:
        return {"error": ve.args[0]}
    else:
        return {"hash": txn_hash.hex(), "error": None}
