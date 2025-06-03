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


// نمایش پیام هشدار
function showPanelWarning() {
    const warning = document.getElementById('panel-warning');
    warning.textContent = 'ابتدا پنل باز شده را ببندید';
    setTimeout(() => {
        warning.textContent = '';
    }, 3000);
}
//بررسی باز بودن پنل دیگر
function isAnyPanelOpen() {
    return (
        document.getElementById('register-employee-panel').style.display === 'block' ||
        document.getElementById('delete-employee-panel').style.display === 'block' ||
        document.getElementById('edit-employee-panel').style.display === 'block' ||
        document.getElementById('orders-panel').style.display === 'block' ||
        document.getElementById('products-panel').style.display === 'block'
    );
}


//ثبت کارمند جدید
function toggleRegisterPanel() {
    const panel = document.getElementById('register-employee-panel');
    // اگر خودش بازه، ببند
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }
    // اگه پنل دیگه‌ای بازه، هشدار بده
    if (isAnyPanelOpen()) {
        showPanelWarning();
        return;
    }
    // در غیر این صورت بازش کن
    panel.style.display = 'block';
    clearMessages();
}

function clearMessages() {
    document.getElementById('employee-error').textContent = '';
    document.getElementById('employee-success').textContent = '';
}

function submitRegisterEmployee() {
    const name = document.getElementById('employee-name').value.trim();
    const family = document.getElementById('employee-family').value.trim();
    const national_id = document.getElementById('employee-national-id').value.trim();
    const phone = document.getElementById('employee-phone').value.trim();
    const username = document.getElementById('employee-username').value.trim();
    const password = document.getElementById('employee-password').value.trim();

    clearMessages();

    if (!name || !family || !national_id || !phone || !username || !password) {
        document.getElementById('employee-error').textContent = 'لطفاً تمام فیلدها را پر کنید.';
        return;
    }

    fetch('/api/manager/register-employee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name,
            family,
            national_id,
            phone,
            username,
            password
        })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
        if (status === 201) {
            document.getElementById('employee-success').textContent = 'مدیر با موفقیت ثبت شد.';
            document.getElementById('register-employee-panel').reset(); // در صورت تمایل فرم را پاک کن
        } else {
            document.getElementById('employee-error').textContent = body.error || 'خطایی رخ داده است.';
        }
    })
    .catch(err => {
        document.getElementById('employee-error').textContent = 'مشکلی در ارتباط با سرور به وجود آمده است.';
        console.error(err);
    });
}

// پنل لیست سفارشات 
function hideOrdersPanel() {
    document.getElementById('orders-panel').style.display = 'none';
}
function toggleOrdersPanel() {
    const panel = document.getElementById('orders-panel');

    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }

    if (isAnyPanelOpen()) {
        showPanelWarning();
        return;
    }

    panel.style.display = 'block';
    clearOrdersMessages();

    fetch('/api/manager/orders')
        .then(res => res.json())
        .then(orders => {
            const list = document.getElementById('orders-list');
            list.innerHTML = '';

            orders.forEach(order => {
                const date = new Date(order.time);
                const formattedDate = date.toLocaleString('fa-IR');

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

function clearOrdersMessages() {
    // اگر پیغام خطایی نمایش داده می‌شود
    const warning = document.getElementById('orders-error');
    if (warning) warning.textContent = '';
}


//لیست محصولات
function hideProductsPanel() {
    document.getElementById('products-panel').style.display = 'none';
}
function toggleProductsPanel() {
    const panel = document.getElementById('products-panel');

    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }

    if (isAnyPanelOpen()) {
        showPanelWarning();
        return;
    }

    panel.style.display = 'block';
    clearProductsMessages();
    fetchProductsList();
}

function clearProductsMessages() {
    const error = document.getElementById('products-error');
    if (error) error.textContent = '';
}

function fetchProductsList() {
    fetch('/api/employee/products')
        .then(res => res.json())
        .then(products => {
            const list = document.getElementById('products-list');
            list.innerHTML = '';
            products.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.quantity}</td>
                    <td>${product.price}</td>
                `;
                list.appendChild(row);
            });
        })
        .catch(err => {
            console.error('خطا در دریافت محصولات:', err);
        });
}
function downloadProductsBackup() {
    const link = document.createElement('a');
    link.href = '/api/manager/backup/product';
    link.download = 'product_backup.zip'; // به صورت اتوماتیک توسط سرور تنظیم می‌شود
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
// پنل لیست سفارشات دانلود
function downloadOrdersBackup() {
    const link = document.createElement('a');
    link.href = '/api/manager/backup/order';
    link.download = 'order_backup.zip'; // به صورت اتوماتیک توسط سرور تنظیم می‌شود
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


//حذف کارمند
function hideDeleteEmployeePanel() {
    document.getElementById('delete-employee-panel').style.display = 'none';
}
function toggleDeleteEmployeePanel() {
    const panel = document.getElementById('delete-employee-panel');
    // اگر خودش بازه، ببندش
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }
    // اگه پنل دیگه‌ای باز باشه، هشدار بده
    if (isAnyPanelOpen()) {
        showPanelWarning();
        return;
    }
    panel.style.display = 'block';
    clearDeleteMessages();
    fetchEmployeesList();

}
function clearDeleteMessages() {
    const errorEl = document.getElementById('delete-error');
    const successEl = document.getElementById('delete-success');
    if (errorEl) errorEl.textContent = '';
    if (successEl) successEl.textContent = '';
}

function fetchEmployeesList() {
    fetch('/api/manager/employees')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('employee-list');
            tbody.innerHTML = '';
            data.forEach(emp => {
                const tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${emp.id}</td>
                    <td>${emp.name}</td>
                    <td>${emp.family}</td>
                    <td>${emp.username}</td>
                    <td>${emp.phone}</td>
                    <td>${emp.role}</td>
                    <td><button class="delete-btn" onclick="deleteEmployee(${emp.id}, this)">حذف</button></td>
                `;

                tbody.appendChild(tr);
            });
        });
}

function deleteEmployee(id, btn) {
    if (!confirm('آیا از حذف این کارمند مطمئن هستید؟')) return;

    fetch(`/api/manager/employees/${id}`, {
        method: 'DELETE'
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            const row = btn.closest('tr');
            row.remove();
        } else {
            alert('خطا در حذف کارمند: ' + (result.error || ''));
        }
    });
}

//ویرایش کارمند
function hideEditEmployeePanel() {
    document.getElementById('edit-employee-panel').style.display = 'none';
}

function toggleEditEmployeePanel() {
    const panel = document.getElementById('edit-employee-panel');
    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }
    if (isAnyPanelOpen()) {
        showPanelWarning();
        return;
    }
    panel.style.display = 'block';
    clearEditEmployeeMessages();
    fetchEmployeesForEdit(); // دریافت لیست برای ویرایش
}

function clearEditEmployeeMessages() {
    const errorEl = document.getElementById('edit-employee-error');
    const successEl = document.getElementById('edit-employee-success');
    if (errorEl) errorEl.textContent = '';
    if (successEl) successEl.textContent = '';
}


function closeEditFormPanel() {
  document.getElementById('edit-employee-form-panel').style.display = 'none';
}

function openEditFormPanel(employee) {
  document.getElementById('edit-id').value = employee.id;
  document.getElementById('edit-name').value = employee.name;
  document.getElementById('edit-family').value = employee.family;
  document.getElementById('edit-phone').value = employee.phone;
  document.getElementById('edit-password').value = '';
  document.getElementById('edit-employee-form-panel').style.display = 'block';
}

function fetchEmployeesForEdit() {
  fetch('/api/manager/employees')
    .then(res => res.json())
    .then(data => {
      const tbody = document.getElementById('employee-edit-list');
      tbody.innerHTML = '';
      data.forEach(emp => {
        const row = `<tr>
          <td>${emp.id}</td>
          <td>${emp.name}</td>
          <td>${emp.family}</td>
          <td>${emp.username}</td>
          <td>${emp.phone}</td>
          <td>${emp.role}</td>
          <td><button class="edit-btn" onclick='openEditFormPanel(${JSON.stringify(emp)})'>ویرایش</button></td>
        </tr>`;
        tbody.insertAdjacentHTML('beforeend', row);
      });
    });
}

// فرم ارسال ویرایش
const editForm = document.getElementById('edit-employee-form');
editForm.addEventListener('submit', function(e) {
  e.preventDefault();
  const id = document.getElementById('edit-id').value;
  const name = document.getElementById('edit-name').value;
  const family = document.getElementById('edit-family').value;
  const phone = document.getElementById('edit-phone').value;
  const password = document.getElementById('edit-password').value;

  fetch(`/api/manager/employees/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, family, phone, password })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || data.error);
      if (data.message) {
        closeEditFormPanel();
        fetchEmployeesForEdit();
      }
    });
});

//ناحیه کاربری فعال
document.querySelector('.user-toggle').addEventListener('click', () => {
    const menu = document.getElementById('user-dropdown-menu');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
});

function closeUserDropdown() {
    document.getElementById('user-dropdown-menu').style.display = 'none';
}
function logout() {
    window.location.href = '/login';
}