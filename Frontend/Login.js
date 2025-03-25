function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var errorMessage = document.getElementById("error-message");

    var correctUsername = "admin";
    var correctPassword = "1234";

    if (username === correctUsername && password === correctPassword) {
        window.location.href = "dashboard.html"; // انتقال به صفحه بعدی
    } else {
        errorMessage.innerHTML = "!نام کاربری یا رمز عبور اشتباه است";

        // حذف پیام خطا بعد از 1.5 ثانیه
        setTimeout(function() {
            errorMessage.innerHTML = "";
        }, 1500);
    }
}
