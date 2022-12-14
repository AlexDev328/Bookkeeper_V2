# Generated by Django 4.1.2 on 2022-10-14 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0004_rename_source_transacton_cost_source_transaction_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cost",
            name="source_transaction",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="source_in_cost",
                to="booking.transaction",
            ),
        ),
    ]
