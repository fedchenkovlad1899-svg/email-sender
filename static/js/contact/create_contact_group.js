document.addEventListener("DOMContentLoaded", async function () {
    const accessToken = localStorage.getItem("access");
    const response = await fetch("/contacts/list/", {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });
    if (!response.ok) {
        document.getElementById("group-error").textContent =
            "Не удалось загрузить контакты";
        document.getElementById("group-error")
            .classList.remove("d-none");
        return;
    }
    const data = await response.json();
    const contacts = data.results || data;
    const contactList = document.getElementById("contact-list");
    contacts.forEach(function (contact) {
        contactList.innerHTML += `
            <div class="form-check">
                <input
                    class="form-check-input contact-checkbox"
                    type="checkbox"
                    value="${contact.id}"
                    id="contact-${contact.id}"
                >
                <label
                    class="form-check-label" for="contact-${contact.id}">${contact.name || "Без имени"} — ${contact.email}</label>
            </div>
        `;
    });

    document.getElementById("save-button").addEventListener("click", async function () {
            const selectedContacts = [];
            document.querySelectorAll(".contact-checkbox:checked").forEach(function (checkbox) {
                selectedContacts.push(Number(checkbox.value));
            });
            const response = await fetch("/groups/create/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + accessToken
                },
                body: JSON.stringify({
                    title: document.getElementById("title").value,
                    description:
                        document.getElementById("description").value,
                    contacts: selectedContacts
                })
            });
            if (response.ok) {
                window.location.href =
                    "/email_sender/contact/group";
            } else {
                document.getElementById("group-error").textContent =
                    "Не удалось создать группу";

                document.getElementById("group-error")
                    .classList.remove("d-none");
            }
        });
});