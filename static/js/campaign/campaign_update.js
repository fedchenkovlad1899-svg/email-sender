document.addEventListener("DOMContentLoaded", async function () {
    const token = localStorage.getItem("access");
    const campaignId = document.getElementById("campaign-id").value;

    const campaign = await loadData(`/campaigns/${campaignId}/`, token);
    const templates = await loadData("/messages/", token);
    const groups = await loadData("/groups/", token);
    const contacts = await loadData("/contacts/list/", token);

    fillSelect("template", templates);
    fillSelect("contact-group", groups);
    fillContacts(contacts, campaign.contacts);

    document.getElementById("title").value = campaign.title;
    document.getElementById("template").value = campaign.template;
    document.getElementById("contact-group").value =
        campaign.contact_group || "";

    if (campaign.scheduled_at) {
        document.getElementById("scheduled-at").value =
            campaign.scheduled_at.slice(0, 16);
    }

    document
        .getElementById("save-button")
        .addEventListener("click", function () {
            updateCampaign(token, campaignId);
        });
});


async function loadData(url, token) {
    const response = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await response.json();
    return data.results || data;
}


function fillSelect(elementId, items) {
    const select = document.getElementById(elementId);

    items.forEach(function (item) {
        select.innerHTML += `
            <option value="${item.id}">
                ${item.title}
            </option>
        `;
    });
}


function fillContacts(contacts, selectedContacts) {
    const contactList = document.getElementById("contact-list");

    contacts.forEach(function (contact) {
        const checked = selectedContacts.includes(contact.id)
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
}


async function updateCampaign(token, campaignId) {
    const contacts = Array.from(
        document.querySelectorAll(".contact-checkbox:checked")
    ).map(function (checkbox) {
        return Number(checkbox.value);
    });

    const response = await fetch(
        `/campaigns/${campaignId}/update/`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                title: document.getElementById("title").value,
                template: document.getElementById("template").value,
                contact_group:
                    document.getElementById("contact-group").value || null,
                contacts: contacts,
                scheduled_at:
                    document.getElementById("scheduled-at").value || null
            })
        }
    );

    if (response.ok) {
        window.location.href = "/email_sender/campaign";
        return;
    }

    const error = await response.json();
    const errorElement = document.getElementById("campaign-error");

    errorElement.textContent =
        error.detail ||
        error.non_field_errors?.[0] ||
        "Не удалось изменить рассылку";

    errorElement.classList.remove("d-none");
}