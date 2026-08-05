document.addEventListener("DOMContentLoaded", async function () {
    const contactId = document.getElementById("contact-id").value;
    const accessToken = localStorage.getItem("access");
    const response = await fetch(`/contacts/${contactId}/`, {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });
    if (!response.ok) {
        document.getElementById("contact-error").textContent =
            "Не удалось загрузить контакт";
        document.getElementById("contact-error")
            .classList.remove("d-none");
        return;
    }
    const contact = await response.json();
    document.getElementById("name").value = contact.name || "";
    document.getElementById("email").value = contact.email || "";
    document.getElementById("description").value = contact.description || "";
    document.getElementById("save-button").addEventListener("click", async function () {
            const response = await fetch(`/contacts/${contactId}/update/`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + accessToken
                    },
                    body: JSON.stringify({
                        name: document.getElementById("name").value,
                        email: document.getElementById("email").value,
                        description:
                            document.getElementById("description").value
                    })
                }
            );
            if (response.ok) {
                window.location.href = "/email_sender/contact/";
            } else {
                document.getElementById("contact-error").textContent =
                    "Не удалось изменить контакт";
                document.getElementById("contact-error")
                    .classList.remove("d-none");
            }
        });
});
