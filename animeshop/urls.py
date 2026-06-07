"""
animeshop/urls.py

Root URL configuration for the animeshop project.

Pattern overview
----------------
    /           → store app (homepage, catalogue, detail, search)
    /admin/     → Django admin panel

Static / media files
--------------------
    During development (DEBUG=True) Django itself serves files under
    MEDIA_URL via django.conf.urls.static.static().
    In production, delegate to Nginx / Whitenoise instead.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ── Admin customisation ───────────────────────────────────────────────────────
admin.site.site_header  = "AnimeShop Administration"
admin.site.site_title   = "AnimeShop Admin"
admin.site.index_title  = "Welcome to the AnimeShop Admin Panel"

# ── URL patterns ──────────────────────────────────────────────────────────────
urlpatterns = [
    # Django admin — always keep before the catch-all store include
    path("admin/", admin.site.urls),

    # Accounts app
    path("accounts/", include("accounts.urls", namespace="accounts")),

    # Store app — mounted at the root so store URLs have no prefix
    # All store URLs are namespaced under "store" (set in store/urls.py)
    path("", include("store.urls", namespace="store")),
]

# ── Development media serving ─────────────────────────────────────────────────
# Appends a route that serves MEDIA_ROOT files at MEDIA_URL only when
# DEBUG is True.  This should NEVER be used in production.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
