"""
Data migration: seed the six default product categories.

These match the frontend navigation links in base.html:
    Hoodies · Posters · Figurines · Keychains · T-Shirts · Joggers

Safe to re-run — uses get_or_create so existing rows are not duplicated.
"""

from django.db import migrations
from django.utils.text import slugify


# The categories shown in the navbar (base.html lines 693-698)
DEFAULT_CATEGORIES = [
    {
        "name": "Hoodies",
        "slug": "hoodies",
        "description": "Anime-themed hoodies and zip-ups for every season.",
    },
    {
        "name": "Posters",
        "slug": "posters",
        "description": "High-quality anime posters and art prints.",
    },
    {
        "name": "Figurines",
        "slug": "figurines",
        "description": "Collectible anime figurines and statues.",
    },
    {
        "name": "Keychains",
        "slug": "keychains",
        "description": "Cute and detailed anime keychains.",
    },
    {
        "name": "T-Shirts",
        "slug": "t-shirts",
        "description": "Stylish anime graphic tees for everyday wear.",
    },
    {
        "name": "Joggers",
        "slug": "joggers",
        "description": "Comfortable anime-themed joggers and track pants.",
    },
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    for cat in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(
            slug=cat["slug"],
            defaults={"name": cat["name"], "description": cat["description"]},
        )


def unseed_categories(apps, schema_editor):
    Category = apps.get_model("store", "Category")
    slugs = [c["slug"] for c in DEFAULT_CATEGORIES]
    Category.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, unseed_categories),
    ]
