const token = localStorage.getItem("access");

let previousUrl = null;
let nextUrl = null;
let currentPage = 1;

document.addEventListener("DOMContentLoaded", function () {
    loadTemplates("/messages/?ordering=title");


    document.getElementById("search-button").addEventListener("click", function () {
            currentPage = 1;
            loadFilteredTemplates();
        });


    document.getElementById("reset-button").addEventListener("click", function () {
            document.getElementById("search-input").value = "";
            document.getElementById("ordering").value = "title";
            currentPage = 1;
            loadTemplates("/messages/?ordering=title");
        });


    document.getElementById("previous-button").addEventListener("click", function () {
            if (previousUrl) {
                currentPage--;
                loadTemplates(previousUrl);
            }
        });


    document.getElementById("next-button").addEventListener("click", function () {
            if (nextUrl) {
                currentPage++;
                loadTemplates(nextUrl);
            }
        });
});


function loadFilteredTemplates() {
    const search = document.getElementById("search-input").value.trim();
    const ordering = document.getElementById("ordering").value;
    const params = new URLSearchParams();
    if (search) {
        params.append("search", search);
    }
    if (ordering) {
        params.append("ordering", ordering);
    }
    loadTemplates("/messages/?" + params.toString());
}


async function loadTemplates(url) {
    const response = await fetch(url, {
        headers: {
            "Authorization":
                "Bearer " + token
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
    previousUrl = data.previous || null;
    nextUrl = data.next || null;
    const templateList = document.getElementById("template-list");
    templateList.innerHTML = "";
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
    if (templates.length === 0) {

        templateList.innerHTML = `
            <tr>
                <td colspan="4" class="text-center">
                    Шаблоны не найдены
                </td>
            </tr>
        `;
    }



    document.getElementById("previous-button").disabled =!previousUrl;
    document.getElementById("next-button").disabled =!nextUrl;
    const total = data.count ?? templates.length;
    const totalPages =
        Math.max(
            1,
            Math.ceil(total / 20)
        );
    document.getElementById("page-info").textContent = `Страница ${currentPage} из ${totalPages}`;
}



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
                    "Bearer " + token
            }
        }
    );
    if (response.ok) {
        window.location.reload();
    } else {
        alert("Не удалось удалить шаблон");
    }
}