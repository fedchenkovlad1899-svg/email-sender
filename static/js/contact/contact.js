const token = localStorage.getItem("access");

let previousUrl = null;
let nextUrl = null;
let currentPage = 1;

document.addEventListener("DOMContentLoaded", function () {
    loadContacts("/contacts/list/?ordering=name");
    document.getElementById("search-button").addEventListener("click", function () {
            currentPage = 1;
            loadFilteredContacts();
        });

    document.getElementById("reset-button").addEventListener("click", function () {
            document.getElementById("search-input").value = "";
            document.getElementById("ordering").value = "name";
            currentPage = 1;
            loadContacts("/contacts/list/?ordering=name");
        });

    document.getElementById("previous-button").addEventListener("click", function () {
            if (previousUrl) {
                currentPage--;
                loadContacts(previousUrl);
            }
        });

    document.getElementById("next-button")
        .addEventListener("click", function () {
            if (nextUrl) {
                currentPage++;
                loadContacts(nextUrl);
            }
        });
});


function loadFilteredContacts() {
    const search = document.getElementById("search-input").value.trim();
    const ordering = document.getElementById("ordering").value;
    const params = new URLSearchParams();
    if (search) {
        params.append("search", search);
    }
    if (ordering) {
        params.append("ordering", ordering);
    }
    loadContacts("/contacts/list/?" + params.toString());
}
async function loadContacts(url) {
    const response = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + token
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
    previousUrl = data.previous || null;
    nextUrl = data.next || null;
    const contactList = document.getElementById("contact-list");
    contactList.innerHTML = "";

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
    if (contacts.length === 0) {
        contactList.innerHTML = `
            <tr>
                <td colspan="5" class="text-center">Контакты не найдены</td>
            </tr>
        `;
    }
    document.getElementById("previous-button").disabled =!previousUrl;
    document.getElementById("next-button").disabled =!nextUrl;
    const total = data.count ?? contacts.length;
    const totalPages =Math.max(1,Math.ceil(total / 20));
    document.getElementById("page-info").textContent = `Страница ${currentPage} из ${totalPages}`;
}

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
                    "Bearer " + token
            }
        }
    );
    if (response.ok) {
        window.location.reload();
    } else {
        alert("Не удалось удалить контакт");
    }
}