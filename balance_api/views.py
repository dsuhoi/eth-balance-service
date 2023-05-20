import logging

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from balance_api.models import Wallet
from balance_api.serializers import (WalletRequestSerializer,
                                     WalletResponseSerializer,
                                     WalletSimpleResponseSerializer)
from balance_api.wallet_operations import create_wallet, get_balance

logger = logging.getLogger(__name__)


# Create your views here.
@extend_schema(tags=["wallets"])
class WalletViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint for operations with Crypto Wallet
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletRequestSerializer
    permission_classes = []

    @extend_schema(
        description="Getting all crypto wallets.",
        responses=WalletResponseSerializer,
    )
    def list(self, request):
        logger.info(request)
        data = [
            {
                "id": w.pk,
                "currency": w.currency,
                "public_key": w.public_key,
                "balance": get_balance(w.public_key, w.currency).get("balance"),
            }
            for w in Wallet.objects.all()
        ]
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Creating crypto wallet.",
        request=WalletRequestSerializer,
        responses=WalletSimpleResponseSerializer,
    )
    def create(self, request):
        logger.info(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pub, priv = create_wallet().values()
            inst = Wallet.objects.create(
                currency=serializer.data.get("currency").lower(),
                public_key=pub,
                private_key=priv,
            )
            return Response(
                data={
                    "id": inst.pk,
                    "currency": inst.currency,
                    "public_key": inst.public_key,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
