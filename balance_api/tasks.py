from celery import shared_task

from balance_api.wallet_operations import get_balance


@shared_task
def get_wallet(wallet: dict[str, int | str]) -> dict[str, int | str | float]:
    return {
        **wallet,
        "balance": get_balance(wallet["public_key"], wallet["currency"]).get("balance"),
    }
