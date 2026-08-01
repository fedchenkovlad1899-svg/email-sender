document.getElementById("save-button").addEventListener("click", async function () {
    const response = await fetch("/contacts/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access")
        },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            description: document.getElementById("description").value
        })
    });

    const message = document.getElementById("message");
    if (response.ok) {
        window.location.href = "/email_sender/contact/";
    } else {
        message.className = "alert alert-danger";
        message.textContent = "Не удалось создать контакт";
    }
});