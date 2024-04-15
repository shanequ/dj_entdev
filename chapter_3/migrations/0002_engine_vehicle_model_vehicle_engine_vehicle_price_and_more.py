# Generated by Django 4.2.11 on 2024-04-13 06:05

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators


class Migration(migrations.Migration):

    dependencies = [
        ('chapter_3', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine',
            name='vehicle_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_engine', to='chapter_3.vehiclemodel', verbose_name='Model'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engine_vehicle', to='chapter_3.engine', verbose_name='Engine'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='AUD', max_digits=19, null=True, validators=[djmoney.models.validators.MinMoneyValidator({'AUD': 400, 'EUR': 500}), djmoney.models.validators.MaxMoneyValidator({'AUD': 400000, 'EUR': 500000})]),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('AUD', 'AUD $'), ('EUR', 'EUR €')], default='AUD', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_vehicle', to='chapter_3.vehiclemodel', verbose_name='Model'),
        ),
    ]
