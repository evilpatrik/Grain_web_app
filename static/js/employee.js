
document.addEventListener("DOMContentLoaded", function () {
    function updateDateTime() {
        const now = new Date();

        const days = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه'];
        const weekday = days[now.getDay()];

        const faDate = new Intl.DateTimeFormat('fa-IR-u-ca-persian', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        }).formatToParts(now);

        const year = faDate.find(p => p.type === 'year').value;
        const month = faDate.find(p => p.type === 'month').value;
        const day = faDate.find(p => p.type === 'day').value;

        const dateStr = `${year}/${month}/${day}`;

        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const timeStr = `${hours}:${minutes}:${seconds}`;

        const weekdayEl = document.getElementById('weekday');
        const dateEl = document.getElementById('shamsi-date');
        const timeEl = document.getElementById('clock');

        if (weekdayEl && dateEl && timeEl) {
            weekdayEl.textContent = weekday;
            dateEl.textContent = dateStr;
            timeEl.textContent = timeStr;
        }
    }

    updateDateTime();
    setInterval(updateDateTime, 1000);
});





let selectedProductId = null;

function toggleSellPanel() {
    const panel = document.getElementById('sell-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    document.getElementById('sell-form-panel').style.display = 'none';
    fetchProductsSell();
}

function fetchProductsSell() {
    fetch('/api/employee/products')
        .then(res => res.json())
        .then(products => {
            const list = document.getElementById('product-list-sell');
            list.innerHTML = '';

            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>${product.quantity}</td>
                    <td><button onclick="openSellForm(${product.id}, '${product.name}')">فروش</button></td>
                `;
                list.appendChild(row);
            });
        })
        .catch(err => console.error('خطا در دریافت محصولات:', err));
}

function openSellForm(productId, productName) {
    selectedProductId = productId;
    document.getElementById('sell-form-title').textContent = `فروش: ${productName}`;
    document.getElementById('sell-form-panel').style.display = 'block';
}

function submitSale() {
    const quantity = document.getElementById('sell-quantity').value;
    if (!quantity || parseInt(quantity) <= 0) {
        alert('لطفاً مقدار معتبر وارد کنید.');
        return;
    }

    fetch(`/api/employee/products/${selectedProductId}/sell`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        fetchProductsSell(); // بروزرسانی لیست
        document.getElementById('sell-form-panel').style.display = 'none';
    })
    .catch(err => {
        console.error('خطا در فروش محصول:', err);
        alert('خطا در فروش محصول');
    });
}

//خرید غلات
function toggleBuyPanel() {
    const panel = document.getElementById('buy-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    document.getElementById('buy-form-panel').style.display = 'none';
    fetchProductsBuy();
}
function fetchProductsBuy() {
    fetch('/api/employee/products')
        .then(res => res.json())
        .then(products => {
            const list = document.getElementById('product-list-buy');
            list.innerHTML = '';

            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.price}</td>
                    <td>${product.quantity}</td>
                    <td><button onclick="openBuyForm(${product.id}, '${product.name}')">خرید</button></td>
                `;
                list.appendChild(row);
            });
        })
        .catch(err => console.error('خطا در دریافت محصولات:', err));
}
function openBuyForm(productId, productName) {
    selectedProductId = productId;
    document.getElementById('buy-form-title').textContent = `خرید: ${productName}`;
    document.getElementById('buy-form-panel').style.display = 'block';
}

function submitBuy() {
    const quantity = document.getElementById('buy-quantity').value;
    const price = document.getElementById('buy-price').value;

    if (!quantity || parseInt(quantity) <= 0) {
        alert('لطفاً مقدار معتبر وارد کنید.');
        return;
    }

    if (!price || parseInt(price) <= 0) {
        alert('لطفاً قیمت معتبر وارد کنید.');
        return;
    }

    fetch(`/api/employee/products/${selectedProductId}/buy`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity, price })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        fetchProductsBuy(); // بروزرسانی لیست
        document.getElementById('buy-form-panel').style.display = 'none';
    })
    .catch(err => {
        console.error('خطا در خرید محصول:', err);
        alert('خطا در خرید محصول');
    });
}

function toggleNewBuyForm() {
    document.getElementById('new-buy-form-panel').style.display = 'block';
}

function hideNewBuyForm() {
    document.getElementById('new-buy-form-panel').style.display = 'none';
}

function submitNewBuy() {
    const name = document.getElementById('new-buy-name').value;
    const price = parseInt(document.getElementById('new-buy-price').value);
    const quantity = parseInt(document.getElementById('new-buy-quantity').value);

    if (!name || isNaN(price) || isNaN(quantity) || price <= 0 || quantity <= 0) {
        alert('لطفاً تمام فیلدها را به‌درستی پر کنید.');
        return;
    }

    fetch('/api/emplyee/product/new-buy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price, quantity })
    })
    .then(res => {
        if (!res.ok) throw new Error('درخواست ناموفق بود');
        return res.json();
    })
    .then(data => {
        alert(data.message);
        hideNewBuyForm();
        fetchProductsBuy(); // بروزرسانی لیست محصولات
    })
    .catch(err => {
        console.error('خطا:', err);
        alert('خطا در ثبت خرید جدید.');
    });
}

// پنل لیست سفارشات 
function toggleOrdersPanel() {
    const panel = document.getElementById('orders-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';

    fetch('/api/employee/orders')
        .then(res => res.json())
        .then(orders => {
            const list = document.getElementById('orders-list');
            list.innerHTML = '';

            orders.forEach(order => {
                const date = new Date(order.time);  // زمان درست
                const formattedDate = date.toLocaleString('fa-IR');  // فرمت فارسی

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.id}</td>
                    <td>${order.types === 'buy' ? 'خرید' : 'فروش'}</td>
                    <td>${order.name}</td>
                    <td>${order.quantity}</td>
                    <td>${order.price}</td>
                    <td>${order.total_price}</td>
                    <td>${formattedDate}</td>
                `;
                list.appendChild(row);
            });
        })
        .catch(err => {
            console.error('خطا در دریافت سفارشات:', err);
        });
}


