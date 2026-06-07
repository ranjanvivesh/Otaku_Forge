document.addEventListener('DOMContentLoaded', () => {

    // ── 1. Category Filter (Fetch API) ──────────────────────────────
    const categoryPills = document.querySelectorAll('.category-strip .pill');
    const productGrid = document.querySelector('.product-grid');

    const scrollToProducts = () => {
        if (!productGrid) return;
        productGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    // Category pill clicks should reload the page normally.

    // Auto-scroll disabled.

    // ── 2. Quantity Selector ───────────────────────────────────────
    const qtyInput = document.querySelector('.qty-input');
    const btnMinus = document.querySelector('.qty-minus');
    const btnPlus = document.querySelector('.qty-plus');

    if (qtyInput && btnMinus && btnPlus) {
        btnMinus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value) || 1;
            if (val > 1) qtyInput.value = val - 1;
        });

        btnPlus.addEventListener('click', () => {
            let val = parseInt(qtyInput.value) || 1;
            let max = parseInt(qtyInput.getAttribute('max')) || 99;
            if (val < max) qtyInput.value = val + 1;
        });
    }

    const CART_KEY = 'otakuforge_cart';

    const readCart = () => {
        try {
            const stored = localStorage.getItem(CART_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Failed to read cart:', error);
            return [];
        }
    };

    const writeCart = (items) => {
        localStorage.setItem(CART_KEY, JSON.stringify(items));
    };

    const parsePrice = (value) => {
        const normalized = (value || '').toString().replace(/[^0-9.]/g, '').trim();
        return normalized ? parseFloat(normalized) : 0;
    };

    const formatPrice = (value) => {
        const safeValue = Number.isFinite(value) ? value : 0;
        return `INR ${safeValue.toFixed(2)}`;
    };

    const getCartCount = (items) => items.reduce((sum, item) => sum + (item.qty || 0), 0);

    const syncBadge = () => {
        const badge = document.getElementById('cart-count');
        if (!badge) return;
        const count = getCartCount(readCart());
        badge.textContent = count.toString();
    };

    const buildItemFromCard = (btn) => {
        const card = btn.closest('.product-card');
        if (!card) return null;

        const name = card.dataset.productName || card.querySelector('.card-name')?.textContent?.trim() || 'Item';
        const priceText = card.dataset.productPrice || card.querySelector('.card-price')?.textContent || '';
        const price = parsePrice(priceText);
        const category = card.dataset.productCategory || card.querySelector('.card-category')?.textContent?.trim() || '';
        const url = card.dataset.productUrl || card.getAttribute('href') || '';
        const image = card.dataset.productImage || card.querySelector('img')?.getAttribute('src') || '';

        const safeUrl = url && url !== '#' ? url : '';
        const rawId = btn.dataset.productId || card.dataset.productId || safeUrl || name;
        const id = rawId.toString();

        return { id, name, price, category, url, image };
    };

    const buildItemFromDetailForm = (form) => {
        const name = form.dataset.productName || 'Item';
        const price = parsePrice(form.dataset.productPrice || '');
        const category = form.dataset.productCategory || '';
        const url = form.dataset.productUrl || '';
        const image = form.dataset.productImage || '';
        const rawId = form.dataset.productId || url || name;
        const id = rawId.toString();
        return { id, name, price, category, url, image };
    };

    const addItemToCart = (item, qty) => {
        if (!item) return;
        const quantity = Number.isFinite(qty) && qty > 0 ? qty : 1;
        const cart = readCart();
        const existing = cart.find(entry => entry.id === item.id);
        if (existing) {
            existing.qty += quantity;
        } else {
            cart.push({ ...item, qty: quantity });
        }
        writeCart(cart);
        syncBadge();
        renderCart();
    };

    const updateItemQty = (id, delta) => {
        const cart = readCart();
        const item = cart.find(entry => entry.id === id);
        if (!item) return;
        item.qty += delta;
        if (item.qty <= 0) {
            const next = cart.filter(entry => entry.id !== id);
            writeCart(next);
        } else {
            writeCart(cart);
        }
        syncBadge();
        renderCart();
    };

    const setItemQty = (id, qty) => {
        const cart = readCart();
        const item = cart.find(entry => entry.id === id);
        if (!item) return;
        item.qty = Math.max(1, qty);
        writeCart(cart);
        syncBadge();
        renderCart();
    };

    const removeItem = (id) => {
        const cart = readCart().filter(entry => entry.id !== id);
        writeCart(cart);
        syncBadge();
        renderCart();
    };

    const clearCart = () => {
        writeCart([]);
        syncBadge();
        renderCart();
    };

    const renderCart = () => {
        const root = document.querySelector('[data-cart-root]');
        if (!root) return;

        const emptyState = document.querySelector('[data-cart-empty]');
        const filledState = document.querySelector('[data-cart-filled]');
        const tbody = document.querySelector('[data-cart-body]');
        const subtotalEl = document.querySelector('[data-cart-subtotal]');

        const cart = readCart();
        if (!tbody || !subtotalEl || !emptyState || !filledState) return;

        if (cart.length === 0) {
            emptyState.hidden = false;
            filledState.hidden = true;
            subtotalEl.textContent = formatPrice(0);
            tbody.innerHTML = '';
            return;
        }

        emptyState.hidden = true;
        filledState.hidden = false;

        let subtotal = 0;
        tbody.innerHTML = cart.map(item => {
            const lineTotal = item.price * item.qty;
            subtotal += lineTotal;
            const imgHtml = item.image
                ? `<img src="${item.image}" alt="${item.name}" class="cart-thumb" />`
                : `<div class="cart-thumb">🎌</div>`;

            return `
                <tr data-cart-row data-cart-id="${item.id}">
                  <td>
                    <div class="cart-product">
                      ${imgHtml}
                      ${item.url ? `<a href="${item.url}">${item.name}</a>` : `<span>${item.name}</span>`}
                    </div>
                  </td>
                  <td>${formatPrice(item.price)}</td>
                  <td>
                    <div class="qty-selector">
                      <button type="button" class="qty-btn" data-cart-action="decrease">-</button>
                      <input type="number" class="qty-input" value="${item.qty}" min="1" data-cart-qty>
                      <button type="button" class="qty-btn" data-cart-action="increase">+</button>
                    </div>
                  </td>
                  <td class="cart-total">${formatPrice(lineTotal)}</td>
                  <td>
                    <button type="button" class="link-ink" data-cart-action="remove">Remove</button>
                  </td>
                </tr>
            `;
        }).join('');

        subtotalEl.textContent = formatPrice(subtotal);
    };

    document.addEventListener('click', (event) => {
        const btn = event.target.closest('.add-to-cart');
        if (!btn) return;

        event.preventDefault();
        event.stopPropagation();

        const item = buildItemFromCard(btn);
        addItemToCart(item, 1);
    });

    document.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') return;
        const btn = event.target.closest('.add-to-cart');
        if (!btn) return;

        event.preventDefault();
        event.stopPropagation();

        const item = buildItemFromCard(btn);
        addItemToCart(item, 1);
    });

    document.addEventListener('submit', (event) => {
        const form = event.target.closest('.detail-actions');
        if (!form) return;

        event.preventDefault();

        const qtyField = form.querySelector('.qty-input');
        const qty = qtyField ? parseInt(qtyField.value, 10) || 1 : 1;
        const item = buildItemFromDetailForm(form);
        addItemToCart(item, qty);
    });

    const cartRoot = document.querySelector('[data-cart-root]');
    if (cartRoot) {
        cartRoot.addEventListener('click', (event) => {
            const actionBtn = event.target.closest('[data-cart-action]');
            if (!actionBtn) return;

            const row = event.target.closest('[data-cart-row]');
            const id = row?.dataset.cartId;
            if (!id) return;

            if (actionBtn.dataset.cartAction === 'increase') {
                updateItemQty(id, 1);
            }
            if (actionBtn.dataset.cartAction === 'decrease') {
                updateItemQty(id, -1);
            }
            if (actionBtn.dataset.cartAction === 'remove') {
                removeItem(id);
            }
        });

        cartRoot.addEventListener('change', (event) => {
            const input = event.target.closest('[data-cart-qty]');
            if (!input) return;
            const row = event.target.closest('[data-cart-row]');
            const id = row?.dataset.cartId;
            if (!id) return;
            const qty = parseInt(input.value, 10) || 1;
            setItemQty(id, qty);
        });

        const clearBtn = document.querySelector('[data-cart-clear]');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => clearCart());
        }
    }

    window.cartStore = {
        syncBadge,
        renderCart,
        addItemToCart
    };

    syncBadge();
    renderCart();

});
