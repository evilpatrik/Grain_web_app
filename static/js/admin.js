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
    return document.getElementById('register-manager-panel').style.display === 'block' ||
           document.getElementById('backup-panel').style.display === 'block';
}
//ثبت مدیر جدید
function toggleRegisterPanel() {
    const panel = document.getElementById('register-manager-panel');
    const otherPanel = document.getElementById('backup-panel');

    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }
    if (otherPanel.style.display === 'block') {
        showPanelWarning();
        return;
    }
    panel.style.display = 'block';
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
//بک آپ
function showBackupPanel() {
    const panel = document.getElementById('backup-panel');
    const otherPanel = document.getElementById('register-manager-panel');

    if (panel.style.display === 'block') {
        panel.style.display = 'none';
        return;
    }
    if (otherPanel.style.display === 'block') {
        showPanelWarning();
        return;
    }
    panel.style.display = 'block';
}

function hideBackupPanel() {
        document.getElementById("backup-panel").style.display = "none";
    }

    function confirmBackup() {
        // ساخت یک لینک مخفی برای دانلود فایل بکاپ
        const link = document.createElement('a');
        link.href = '/api/admin/backup';
        link.download = 'project_backup.zip';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        hideBackupPanel(); // بستن پنل بعد از کلیک
}
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