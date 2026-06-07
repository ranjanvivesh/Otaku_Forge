"""Admin configuration for the store app.
Provides custom list displays, inlines, and actions for Category and Product models.
"""
from django.contrib import admin
from django.utils.html import format_html
from store.models import Category, Product


# ---------------------------------------------------------------------------
# Inline — show products directly inside the Category admin page
# ---------------------------------------------------------------------------

class ProductInline(admin.TabularInline):
    """
    Displays a compact table of products beneath each Category record,
    allowing quick edits without leaving the category page.
    """
    model          = Product
    extra          = 1                          # one blank row ready to fill
    fields         = ["name", "slug", "price", "stock", "is_available"]
    prepopulated_fields = {"slug": ("name",)}
    show_change_link = True                     # link to full product form


# ---------------------------------------------------------------------------
# CategoryAdmin
# ---------------------------------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.

    Features:
        - slug auto-populated from name
        - inline product list
        - search and ordering
    """

    list_display        = ["name", "slug", "product_count", "created_at"]
    search_fields       = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering            = ["name"]
    inlines             = [ProductInline]

    # ── Custom column: number of products in this category ──

    @admin.display(description="# Products")
    def product_count(self, obj) -> int:
        """Return number of products in a category."""
        return obj.products.count()


# ---------------------------------------------------------------------------
# Custom admin actions
# ---------------------------------------------------------------------------

@admin.action(description="Mark selected products as available")
# Unused args are required by the admin API; suppress lint warnings
# pylint: disable=unused-argument
def make_available(modeladmin, request, queryset):
    queryset.update(is_available=True)


@admin.action(description="Mark selected products as unavailable")
# pylint: disable=unused-argument
def make_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)


# ---------------------------------------------------------------------------
# ProductAdmin
# ---------------------------------------------------------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for the Product model.

    Features:
        - image thumbnail preview in the list view
        - inline price / stock / availability editing
        - filter sidebar (category, availability)
        - slug auto-populated from name
        - bulk actions to toggle availability
        - date hierarchy drill-down
    """

    list_display = [
        "thumbnail_preview",
        "name",
        "category",
        "price",
        "stock",
        "is_available",
        "created_at",
    ]
    list_display_links  = ["thumbnail_preview", "name"]
    list_editable       = ["price", "stock", "is_available"]
    list_filter         = ["is_available", "category", "created_at"]
    list_select_related = ["category"]
    search_fields       = ["name", "description", "category__name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering            = ["-created_at"]
    date_hierarchy      = "created_at"
    actions             = [make_available, make_unavailable]
    readonly_fields     = ["image_preview"]

    # Fields shown on the add / change form, grouped into logical sections
    fieldsets = (
        ("Basic Information", {
            "fields": ("category", "name", "slug", "description"),
        }),
        ("Pricing & Inventory", {
            "fields": ("price", "stock", "is_available"),
        }),
        ("Media", {
            "fields": ("image", "image_preview"),
        }),
    )

    # ── Custom column: small thumbnail in the changelist ────

    @admin.display(description="Image")
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:48px;width:48px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:160px;width:160px;'
                'object-fit:cover;border-radius:8px;border:1px solid #ddd;" />',
                obj.image.url,
            )
        return "—"
