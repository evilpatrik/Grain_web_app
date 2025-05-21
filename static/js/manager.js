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
    const panel = document.getElementById('register-employee-panel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
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