document.getElementById("save-button").addEventListener("click", async function () {

    const response = await fetch("/change_password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access")
        },
        body: JSON.stringify({
            old_password: document.getElementById("old_password").value,
            new_password: document.getElementById("new_password").value
        })
    });
    const message = document.getElementById("message");
    if (response.ok) {
        message.className = "alert alert-success";
        message.textContent = "Пароль успешно изменен";
    } else {
        message.className = "alert alert-danger";
        message.textContent = "Ошибка смены пароля";
    }
});