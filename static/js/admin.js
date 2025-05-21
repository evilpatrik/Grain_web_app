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






function toggleRegisterPanel() {
    const panel = document.getElementById('register-manager-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    clearMessages();
}

function clearMessages() {
    document.getElementById('manager-error').textContent = '';
    document.getElementById('manager-success').textContent = '';
}

function submitRegisterManager() {
    const name = document.getElementById('manager-name').value.trim();
    const family = document.getElementById('manager-family').value.trim();
    const national_id = document.getElementById('manager-national-id').value.trim();
    const phone = document.getElementById('manager-phone').value.trim();
    const username = document.getElementById('manager-username').value.trim();
    const password = document.getElementById('manager-password').value.trim();

    clearMessages();

    if (!name || !family || !national_id || !phone || !username || !password) {
        document.getElementById('manager-error').textContent = 'لطفاً تمام فیلدها را پر کنید.';
        return;
    }

    fetch('/api/admin/register-manager', {
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
            document.getElementById('manager-success').textContent = 'مدیر با موفقیت ثبت شد.';
            document.getElementById('register-manager-panel').reset(); // در صورت تمایل فرم را پاک کن
        } else {
            document.getElementById('manager-error').textContent = body.error || 'خطایی رخ داده است.';
        }
    })
    .catch(err => {
        document.getElementById('manager-error').textContent = 'مشکلی در ارتباط با سرور به وجود آمده است.';
        console.error(err);
    });
}


