from django.db import models


# Create your models here.
class Wallet(models.Model):
    CURRENCY_CHOICES = (("eth", "Ethereum"),)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, null=False, default="eth"
    )
    public_key = models.CharField(max_length=70, unique=True, null=False)
    private_key = models.CharField(max_length=70, unique=True, null=False)

    def __str__(self):
        return f"{self.id} # Public: {self.public_key}"
