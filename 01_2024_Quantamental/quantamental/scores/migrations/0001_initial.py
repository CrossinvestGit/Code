# Generated by Django 5.0.1 on 2024-01-29 16:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                ("price", models.FloatField(null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[("Indoor", "Indoor"), ("Out door", "Out door")],
                        max_length=200,
                        null=True,
                    ),
                ),
                ("description", models.CharField(max_length=200, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("profile_pic", models.ImageField(default="default.jpg", upload_to="")),
                ("name", models.CharField(max_length=200, null=True)),
                ("phone", models.CharField(max_length=200, null=True)),
                ("email", models.CharField(max_length=200, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Out for delivery", "Out for delivery"),
                            ("Delivered", "Delivered"),
                        ],
                        max_length=200,
                        null=True,
                    ),
                ),
                ("note", models.CharField(max_length=100, null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scores.customer",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="scores.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(to="scores.tag"),
        ),
    ]