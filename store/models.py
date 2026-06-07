from django.db import models
from django.urls import reverse


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------

class Category(models.Model):
    """
    Top-level grouping for products.
    The default categories are: Hoodies, Posters, Figurines, Keychains, T-Shirts, Joggers.
    Admin can add more via the Django admin panel.
    """

    # Predefined category name choices
    HOODIES   = "Hoodies"
    POSTERS   = "Posters"
    FIGURINES = "Figurines"
    KEYCHAINS = "Keychains"
    TSHIRTS   = "T-Shirts"
    JOGGERS   = "Joggers"

    NAME_CHOICES = [
        (HOODIES,   "Hoodies"),
        (POSTERS,   "Posters"),
        (FIGURINES, "Figurines"),
        (KEYCHAINS, "Keychains"),
        (TSHIRTS,   "T-Shirts"),
        (JOGGERS,   "Joggers"),
    ]

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Category name (e.g. Hoodies, Posters, Figures, Keychains).",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly identifier — auto-filled in admin.",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional short description shown on the category page.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Category"
        verbose_name_plural = "Categories"
        ordering            = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL for the product list filtered by this category."""
        return reverse("store:product_list") + f"?category={self.slug}"


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class Product(models.Model):
    """
    An individual product available in the store.
    Linked to a Category via a ForeignKey.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        help_text="The category this product belongs to.",
    )
    name = models.CharField(
        max_length=255,
        help_text="Full product name (e.g. 'Naruto Hokage Hoodie').",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly identifier — auto-filled in admin.",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed product description shown on the product page.",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Selling price in INR (e.g. 499.00).",
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Number of units currently available.",
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Product thumbnail — stored under MEDIA_ROOT/products/.",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Uncheck to hide the product from the storefront.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the product was first added.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the most recent update.",
    )

    class Meta:
        verbose_name        = "Product"
        verbose_name_plural = "Products"
        ordering            = ["-created_at"]

    # ── String representation ──────────────────────────────────

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    # ── Helpers ───────────────────────────────────────────────

    def get_absolute_url(self):
        """Canonical URL for the product detail page."""
        return reverse("store:product_detail", kwargs={"slug": self.slug})

    @property
    def is_in_stock(self):
        """True when at least one unit is available."""
        return self.stock > 0

    @property
    def display_price(self):
        """Returns price formatted as a rupee string (e.g. '₹499.00')."""
        return f"₹{self.price:,.2f}"
