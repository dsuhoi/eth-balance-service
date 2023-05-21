import json
import logging
import warnings

import pytest

warnings.filterwarnings("ignore", category=DeprecationWarning)

from unittest import mock

from balance_api.models import Wallet
from balance_api.tasks import get_wallet
from balance_api.views import WalletViewSet
from django.urls import reverse

pytestmark = pytest.mark.django_db

logger = logging.getLogger(__name__)


def mocked_get_balance(address: str, currency: str) -> dict[str, float | str | None]:
    return {"balance": 1.0, "error": None}


def mocked_create_wallet() -> dict[str, str]:
    return {"private_key": "priv_key_hash", "public_key": "pub_key_hash"}


class MockGetWalletDelay:
    def __init__(self, wallet: dict[str, int | str]):
        self.wallet = wallet

    def get(self):
        return {**self.wallet, "balance": mocked_get_balance("", "")}

    def ready(self):
        return True


class TestWalletViewset:
    @mock.patch("balance_api.tasks.get_wallet")
    def test_list(self, mock_delay, rf):
        mock_delay.delay = MockGetWalletDelay

        url = reverse("wallets-list")
        request = rf.get(url)
        for i, adr, priv in [
            (1, "pub1", "priv1"),
            (2, "pub2", "priv2"),
            (3, "pub3", "priv3"),
        ]:
            Wallet.objects.create(
                id=i, currency="eth", public_key=adr, private_key=priv
            )

        view = WalletViewSet.as_view({"get": "list"})

        response = view(request).render()
        result = json.loads(response.content)
        logger.info(result)

        assert response.status_code == 200
        assert result[0].get("public_key") == "pub1"

    @mock.patch(
        "balance_api.wallet_operations.create_wallet", side_effect=mocked_create_wallet
    )
    def test_create(self, mocker, rf):
        url = reverse("wallets-list")
        request = rf.post(
            url, content_type="application/json", data=json.dumps({"currency": "eth"})
        )
        view = WalletViewSet.as_view({"post": "create"})

        response = view(request).render()
        result = json.loads(response.content)

        assert response.status_code == 201
        assert result.get("id") == 1
