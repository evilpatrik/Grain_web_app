
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
    fetchProducts();
}

function fetchProducts() {
    fetch('/api/employee/products')
        .then(res => res.json())
        .then(products => {
            const list = document.getElementById('product-list');
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
        fetchProducts(); // بروزرسانی لیست
        document.getElementById('sell-form-panel').style.display = 'none';
    })
    .catch(err => {
        console.error('خطا در فروش محصول:', err);
        alert('خطا در فروش محصول');
    });
}
