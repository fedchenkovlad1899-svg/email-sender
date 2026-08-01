document.addEventListener("DOMContentLoaded", async function () {

    const groupId = document.getElementById("group-id").value;
    const accessToken = localStorage.getItem("access");
    const errorElement = document.getElementById("group-error");

    const groupResponse = await fetch(`/groups/${groupId}/`, {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });

    const contactsResponse = await fetch("/contacts/list/", {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });

    if (!groupResponse.ok || !contactsResponse.ok) {
        errorElement.textContent = "Не удалось загрузить данные";
        errorElement.classList.remove("d-none");
        return;
    }

    const group = await groupResponse.json();
    const contactsData = await contactsResponse.json();
    const contacts = contactsData.results || contactsData;

    document.getElementById("title").value = group.title || "";
    document.getElementById("description").value =
        group.description || "";

    const contactList = document.getElementById("contact-list");

    contacts.forEach(function (contact) {
        const checked = group.contacts.includes(contact.id)
            ? "checked"
            : "";

        contactList.innerHTML += `
            <div class="form-check">
                <input
                    class="form-check-input contact-checkbox"
                    type="checkbox"
                    value="${contact.id}"
                    id="contact-${contact.id}"
                    ${checked}
                >

                <label
                    class="form-check-label"
                    for="contact-${contact.id}"
                >
                    ${contact.name || "Без имени"} — ${contact.email}
                </label>
            </div>
        `;
    });

    document.getElementById("save-button")
        .addEventListener("click", async function () {

            const selectedContacts = [];

            document.querySelectorAll(
                ".contact-checkbox:checked"
            ).forEach(function (checkbox) {
                selectedContacts.push(Number(checkbox.value));
            });

            const response = await fetch(
                `/groups/${groupId}/update/`,
                {
                    method: "PATCH",
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
                }
            );

            if (response.ok) {
                window.location.href = "/email_sender/contact/group";
            } else {
                errorElement.textContent =
                    "Не удалось изменить группу";

                errorElement.classList.remove("d-none");
            }
        });
});