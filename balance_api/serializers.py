import logging

from rest_framework import serializers

from balance_api.models import Wallet
from balance_api.wallet_operations import create_wallet

logger = logging.getLogger(__name__)


class WalletRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["currency"]


class WalletSimpleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "currency", "public_key"]


class WalletResponseSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=28, decimal_places=18, min_value=0)

    class Meta:
        model = Wallet
        fields = ["id", "currency", "public_key", "balance"]
