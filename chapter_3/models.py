
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.db.models import Count
from django.db.models.functions import Lower
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator


YESNO_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

MAKE_CHOICES = (
    (1, 'Buick'),
    (2, 'Cadillac'),
    (3, 'Chevrolet'),
)

MAKE_CHOICES_DICT = dict(MAKE_CHOICES)


class VehicleModel(models.Model):
    name = models.CharField(
        verbose_name='Model', max_length=75, unique=True,
        blank=True, null=True,  # db_index=True
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(75),
        ]
    )

    make = models.PositiveSmallIntegerField(
        choices=MAKE_CHOICES, blank=True, null=True,
        verbose_name='Vehicle Model Make/Brand',
    )

    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['name',]
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-name'], name='desc_name_idx'),
            models.Index(Lower('name').desc(), name='lower_name_idx'),
        ]


class Engine(models.Model):
    name = models.CharField(
        verbose_name='Engine', max_length=75, blank=True, null=True
    )
    vehicle_model = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Model', related_name='model_engine',
    )



class BuickVehicleModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(make=1)


class ChevyVehicleModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(make=3)


class MakeCounterModel(models.Manager):

    def get_queryset(self):
        return super().get_queryset().values("make").annotate(c=Count("make"))

class Vehicle(models.Model):
    vin = models.CharField(
        verbose_name='VIN', max_length=17, unique=True, blank=True, null=True
    )
    sold = models.BooleanField(
        verbose_name='Sold?', choices=YESNO_CHOICES, blank=True, null=True)
    price = MoneyField(
        max_digits=19, decimal_places=2, default_currency='AUD', null=True,
        validators=[
            MinMoneyValidator({'EUR': 500, 'AUD': 400}),
            MaxMoneyValidator({'EUR': 500_000, 'AUD': 400_000}),
        ]
    )
    vehicle_model = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Model', related_name='model_vehicle',
    )
    engine = models.ForeignKey(
        Engine, on_delete=models.CASCADE, blank=True, null=True,
        verbose_name='Engine', related_name='engine_vehicle',
    )
    make = models.PositiveSmallIntegerField(
        choices=MAKE_CHOICES, blank=True, null=True,
        verbose_name='Vehicle Make/Brand',
    )

    def __str__(self):
        return f'{MAKE_CHOICES_DICT.get(self.make)} {self.vehicle_model.name}'

    def full_vehicle_name(self):
        return f'{self.__str__()} - {self.engine.name}'

    @property
    def fullname(self):
        return f'{self.__str__()} - {self.engine.name}'

    buicks = BuickVehicleModel()
    chevys = ChevyVehicleModel()
    objects = models.Manager()
    make_counter = MakeCounterModel()


class Seller(AbstractUser):
    name = models.CharField(
        verbose_name='Seller Name', max_length=150, blank=True, null=True
    )
    vehicle = models.ManyToManyField(
        Vehicle, blank=True, verbose_name='Vehicles',
        related_name='vehicle_sellers', related_query_name='vehicle_seller',
    )
