document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/messages/", {
        headers: {
            "Authorization":
                "Bearer " + localStorage.getItem("access")
        }
    });

    if (!response.ok) {
        const errorElement =
            document.getElementById("template-error");
        errorElement.textContent =
            "Не удалось загрузить шаблоны";
        errorElement.classList.remove("d-none");
        return;
    }

    const data = await response.json();
    const templates = data.results || data;
    const templateList = document.getElementById("template-list");
    templates.forEach(function (template) {
        templateList.innerHTML += `
            <tr>
                <td>${template.title}</td>
                <td>${template.subject}</td>
                <td>
                    ${new Date(
                        template.created_at
                    ).toLocaleString("ru-RU")}
                </td>
                <td>
                    <a href="/email_sender/message_template/${template.id}/update"class="btn btn-sm btn-primary">Изменить</a>
                    <button type="button" class="btn btn-sm btn-danger" onclick="deleteTemplate(${template.id})">Удалить</button>
                </td>
            </tr>
        `;
    });
});


async function deleteTemplate(templateId) {
    if (!confirm("Удалить шаблон письма?")) {
        return;
    }
    const response = await fetch(
        `/messages/${templateId}/delete/`,
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
        alert("Не удалось удалить шаблон");
    }
}