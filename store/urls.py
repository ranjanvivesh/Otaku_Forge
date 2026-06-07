"""
store/urls.py

URL patterns for the store app.
All names are prefixed with the app namespace "store" (set via app_name).

Usage in templates:
    {% url 'store:home' %}
    {% url 'store:product_list' %}
    {% url 'store:product_list' %}?category=hoodies&sort=price_asc
    {% url 'store:category_detail' slug=category.slug %}
    {% url 'store:product_detail' slug=product.slug %}
    {% url 'store:search' %}?q=naruto
"""

from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    # ── Homepage ──────────────────────────────────────────────────────────────
    # GET /
    # View  : store.views.home
    # Shows : featured products + category strip
    path(
        "",
        views.home,
        name="home",
    ),

    # ── Full product catalogue ────────────────────────────────────────────────
    # GET /products/
    # GET /products/?category=<slug>
    # GET /products/?sort=newest|price_asc|price_desc|name_asc
    # GET /products/?page=<n>
    # View  : store.views.product_list
    path(
        "products/",
        views.product_list,
        name="product_list",
    ),

    # ── Hoodies landing page ───────────────────────────────────────────────
    # GET /hoodies/
    # View  : store.views.hoodies_page
    path(
        "hoodies/",
        views.hoodies_page,
        name="hoodies",
    ),

    # ── Posters landing page ───────────────────────────────────────────────
    # GET /posters/
    # View  : store.views.posters_page
    path(
        "posters/",
        views.posters_page,
        name="posters",
    ),

    # ── Figurines landing page ─────────────────────────────────────────────
    # GET /figurines/
    # View  : store.views.figurines_page
    path(
        "figurines/",
        views.figurines_page,
        name="figurines",
    ),

    # ── Keychains landing page ─────────────────────────────────────────────
    # GET /keychains/
    # View  : store.views.keychains_page
    path(
        "keychains/",
        views.keychains_page,
        name="keychains",
    ),

    # ── T-Shirts landing page ─────────────────────────────────────────────
    # GET /tshirts/
    # View  : store.views.tshirts_page
    path(
        "tshirts/",
        views.tshirts_page,
        name="tshirts",
    ),

    # ── Joggers landing page ─────────────────────────────────────────────
    # GET /joggers/
    # View  : store.views.joggers_page
    path(
        "joggers/",
        views.joggers_page,
        name="joggers",
    ),

    # ── Category detail (clean URL) ───────────────────────────────────────────
    # GET /category/<slug>/
    # View  : store.views.category_detail
    # Better than ?category= for SEO and sharing
    path(
        "category/<slug:slug>/",
        views.category_detail,
        name="category_detail",
    ),

    # ── Product detail ────────────────────────────────────────────────────────
    # GET /products/<slug>/
    # View  : store.views.product_detail
    # The <slug:slug> converter rejects any path that is not slug-safe
    path(
        "products/<slug:slug>/",
        views.product_detail,
        name="product_detail",
    ),

    # ── Search ────────────────────────────────────────────────────────────────
    # GET /search/?q=<term>
    # View  : store.views.search
    # Redirects to product_list when q is empty
    path(
        "search/",
        views.search,
        name="search",
    ),

    # ── Cart ──────────────────────────────────────────────────────────────────
    path(
        "cart/",
        views.cart_detail,
        name="cart_detail",
    ),
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
]
