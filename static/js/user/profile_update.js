document.addEventListener("DOMContentLoaded", async function () {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        window.location.href = "/email_sender/login/";
        return;
    }
    const response = await fetch("/profile/", {
        headers: {"Authorization": "Bearer " + accessToken}
    });

    if (!response.ok) {
        alert("Не удалось получить профиль");
        return;
    }
    const user = await response.json();
    document.getElementById("email").value = user.email;
    document.getElementById("first_name").value = user.first_name;
    document.getElementById("last_name").value = user.last_name;



    document.getElementById("save-button").addEventListener("click", async function () {
    const accessToken = localStorage.getItem("access");
    const response = await fetch("/profile/", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            first_name: document.getElementById("first_name").value,
            last_name: document.getElementById("last_name").value
        })
    });

    const message = document.getElementById("message");
    if (response.ok) {
        message.className = "alert alert-success";
        message.textContent = "Профиль обновлен";
        setTimeout(function () {
            window.location.href = "/email_sender/profile/";
        }, 1000);
    } else {
        message.className = "alert alert-danger";
        message.textContent = "Ошибка сохранения";
    }
});
});