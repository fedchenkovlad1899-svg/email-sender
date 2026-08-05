document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/contacts/list/", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("access")
        }
    });

    if (!response.ok) {
        document.getElementById("contact-error").textContent =
            "Не удалось загрузить контакты";
        document.getElementById("contact-error")
            .classList.remove("d-none");
        return;
    }
    const data = await response.json();
    const contacts = data.results || data;
    const contactList = document.getElementById("contact-list");

    contacts.forEach(function (contact) {
        contactList.innerHTML += `
            <tr>
                <td>${contact.name || ""}</td>
                <td>${contact.email}</td>
                <td>${contact.description || ""}</td>
                <td>${new Date(contact.created_at).toLocaleString("ru-RU")}</td>
                <td>
                    <a href="/email_sender/contact/${contact.id}/update"class="btn btn-sm btn-primary">Изменить</a>
                <button class="btn btn-sm btn-danger"onclick="deleteContact(${contact.id})">Удалить</button>
                </td>
            </tr>
        `;
    });
});


async function deleteContact(contactId) {
    if (!confirm("Удалить контакт?")) {
        return;
    }
    const response = await fetch(
        `/contacts/${contactId}/delete/`,
        {
            method: "DELETE",
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("access")
            }
        }
    );
    if (response.ok) {
        window.location.reload();
    } else {
        alert("Не удалось удалить контакт");
    }
}