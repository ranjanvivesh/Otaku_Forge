"""
store/views.py

Function-based views for the AnimeShop store app.

Views
-----
    home             — Landing page: featured products + all categories
    product_list     — Full catalogue with optional ?category= / ?q= filters
    category_detail  — Clean URL view for a single category  (/category/<slug>/)
    product_detail   — Individual product page with related products
    search           — Simple keyword search across name + description
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages

from .models import Category, Product


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _paginate(queryset, request, per_page=12):
    """
    Wraps Django's Paginator.
    Returns a Page object for the current ?page= query param.
    Falls back to page 1 for invalid / out-of-range values.
    """
    paginator = Paginator(queryset, per_page)
    page_num  = request.GET.get("page", 1)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


# ---------------------------------------------------------------------------
# home
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def home(request):
    """
    Landing page.

    Context
    -------
        featured_products  — 8 most-recently-added available products
        categories         — all Category objects (for the category strip)
        new_arrivals       — 4 newest products (hero highlight)
    """
    all_products = Product.objects.filter(is_available=True).select_related("category")

    featured_products = all_products[:8]
    new_arrivals      = all_products[:4]
    categories        = Category.objects.all()

    context = {
        "featured_products": featured_products,
        "new_arrivals":      new_arrivals,
        "categories":        categories,
    }
    return render(request, "store/home.html", context)


# ---------------------------------------------------------------------------
# hoodies_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def hoodies_page(request):
    """
    Hoodies landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.HOODIES).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/hoodies.html", context)


# ---------------------------------------------------------------------------
# posters_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def posters_page(request):
    """
    Posters landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.POSTERS).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/posters.html", context)


# ---------------------------------------------------------------------------
# figurines_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def figurines_page(request):
    """
    Figurines landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.FIGURINES).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/figurines.html", context)


# ---------------------------------------------------------------------------
# keychains_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def keychains_page(request):
    """
    Keychains landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.KEYCHAINS).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/keychains.html", context)


# ---------------------------------------------------------------------------
# tshirts_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def tshirts_page(request):
    """
    T-Shirts landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.TSHIRTS).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/tshirts.html", context)


# ---------------------------------------------------------------------------
# joggers_page
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def joggers_page(request):
    """
    Joggers landing page backed by Product data.
    """
    category = Category.objects.filter(name__iexact=Category.JOGGERS).first()
    products = Product.objects.filter(is_available=True, category=category).select_related("category") if category else Product.objects.none()

    context = {
        "category": category,
        "products": products,
        "product_count": products.count(),
    }
    return render(request, "store/joggers.html", context)


# ---------------------------------------------------------------------------
# product_list
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def product_list(request):
    """
    Full product catalogue.

    Supports two optional GET parameters:
        ?category=<slug>   — filter by category
        ?sort=<option>     — ordering (newest | price_asc | price_desc)

    The active_category, sort, and sort_label values are echoed back into
    the context so templates can reflect the current state in the UI.

    Context
    -------
        page_obj          — paginated Page of Product objects
        categories        — all Category objects
        active_category   — the Category being filtered on (or None)
        sort              — current sort key string
        sort_label        — human-readable sort label
    """

    # -- Collect all available products with one JOIN to avoid N+1 --
    products = Product.objects.filter(is_available=True).select_related("category")

    # -- Category filter --
    category_slug   = request.GET.get("category", "").strip()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # -- Sorting --
    SORT_OPTIONS = {
        "newest":     ("-created_at", "Newest First"),
        "price_asc":  ("price",       "Price: Low → High"),
        "price_desc": ("-price",      "Price: High → Low"),
        "name_asc":   ("name",        "Name: A → Z"),
    }

    sort       = request.GET.get("sort", "newest")
    sort_field, sort_label = SORT_OPTIONS.get(sort, SORT_OPTIONS["newest"])
    products   = products.order_by(sort_field)

    # -- Paginate (12 per page) --
    page_obj = _paginate(products, request, per_page=12)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from django.http import JsonResponse
        data = [
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "price": p.display_price,
                "image_url": p.image.url if p.image else None,
                "category_name": p.category.name,
                "is_in_stock": p.is_in_stock
            }
            for p in page_obj.object_list
        ]
        return JsonResponse({"products": data})

    context = {
        "page_obj":        page_obj,
        "categories":      Category.objects.all(),
        "active_category": active_category,
        "sort":            sort,
        "sort_label":      sort_label,
        "sort_options":    {k: v[1] for k, v in SORT_OPTIONS.items()},
    }
    return render(request, "store/product_list.html", context)


# ---------------------------------------------------------------------------
# category_detail
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def category_detail(request, slug):
    """
    Dedicated view for a single category at /category/<slug>/.

    Cleaner than the query-param approach — better for SEO and sharing.
    Internally re-uses the same product_list template but passes the
    category object directly so the page heading and meta title are richer.

    Context
    -------
        category    — the Category object
        page_obj    — paginated Page of Products in this category
        categories  — all Category objects (for sidebar / filter strip)
    """
    category = get_object_or_404(Category, slug=slug)
    products = (
        Product.objects
        .filter(category=category, is_available=True)
        .select_related("category")
        .order_by("-created_at")
    )
    page_obj = _paginate(products, request, per_page=12)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        from django.http import JsonResponse
        data = [
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "price": p.display_price,
                "image_url": p.image.url if p.image else None,
                "category_name": p.category.name,
                "is_in_stock": p.is_in_stock
            }
            for p in page_obj.object_list
        ]
        return JsonResponse({"products": data})

    context = {
        "category":        category,
        "page_obj":        page_obj,
        "active_category": category,
        "categories":      Category.objects.all(),
    }
    return render(request, "store/category_detail.html", context)


# ---------------------------------------------------------------------------
# product_detail
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def product_detail(request, slug):
    """
    Individual product page.

    Fetches the product by slug and checks is_available so that hidden
    products return a 404 rather than leaking their data.

    Also pulls up to 4 related products from the same category, excluding
    the current product, to power the 'You Might Also Like' section.

    Context
    -------
        product  — the Product object
        related  — up to 4 related Product objects (same category)
    """
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_available=True,
    )

    related = (
        Product.objects
        .filter(category=product.category, is_available=True)
        .exclude(pk=product.pk)
        .order_by("-created_at")[:4]
    )

    context = {
        "product": product,
        "related": related,
    }
    return render(request, "store/product_detail.html", context)


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------

@ensure_csrf_cookie
def search(request):
    """
    Keyword search view — accessible at /search/?q=<term>.

    Searches across Product.name and Product.description using a
    case-insensitive OR query.  Redirects to product_list when the
    query is empty so the user isn't shown a blank results page.

    Context
    -------
        page_obj    — paginated Page of matching Product objects
        query       — the raw search string (echoed into the template)
        result_count — total number of matches (before pagination)
    """
    query = request.GET.get("q", "").strip()

    if not query:
        return redirect("store:product_list")

    products = (
        Product.objects
        .filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True,
        )
        .select_related("category")
        .order_by("-created_at")
    )

    result_count = products.count()
    page_obj     = _paginate(products, request, per_page=12)

    context = {
        "page_obj":     page_obj,
        "query":        query,
        "result_count": result_count,
    }
    return render(request, "store/search_results.html", context)


# ---------------------------------------------------------------------------
# Cart
# ---------------------------------------------------------------------------

def cart_detail(request):
    """
    Shows items currently in the session-based cart.
    """
    cart = request.session.get("cart", {})
    
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    cart_items = []
    total_price = 0
    
    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        total_price += total
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "total": total
        })
        
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }
    return render(request, "store/cart.html", context)

def add_to_cart(request, product_id):
    """
    Adds a product to the cart session or updates its quantity.
    """
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = request.session.get("cart", {})
    
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
        except ValueError:
            quantity = 1
            
        quantity = max(1, min(quantity, product.stock))
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            new_qty = cart[product_id_str] + quantity
            cart[product_id_str] = min(new_qty, product.stock)
        else:
            cart[product_id_str] = quantity
            
        request.session["cart"] = cart
        messages.success(request, f"Added {product.name} to your cart.")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            from django.http import JsonResponse
            cart_count = sum(cart.values())
            return JsonResponse({"cart_count": cart_count})

    return redirect("store:cart_detail")

def remove_from_cart(request, product_id):
    """
    Removes a product entirely from the cart session.
    """
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session["cart"] = cart
        messages.info(request, "Item removed from cart.")
        
    return redirect("store:cart_detail")

