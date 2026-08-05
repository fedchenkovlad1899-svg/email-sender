document.addEventListener("DOMContentLoaded", async function () {
    const accessToken = localStorage.getItem("access");
    const groupSelect = document.getElementById("group");
    const errorElement = document.getElementById("import-error");
    const response = await fetch("/groups/", {
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    });
    if (!response.ok) {
        errorElement.textContent =
            "Не удалось загрузить группы";
        errorElement.classList.remove("d-none");
        return;
    }
    const data = await response.json();
    const groups = data.results || data;
    groups.forEach(function (group) {
        groupSelect.innerHTML += `
            <option value="${group.id}">
                ${group.title}
            </option>
        `;
    });

    document.getElementById("import-button")
        .addEventListener("click", async function () {
            const file = document.getElementById("file").files[0];
            const groupId = groupSelect.value;
            const successElement =
                document.getElementById("import-success");
            successElement.classList.add("d-none");
            errorElement.classList.add("d-none");
            if (!file) {
                errorElement.textContent = "Выберите файл";
                errorElement.classList.remove("d-none");
                return;
            }
            const formData = new FormData();
            formData.append("file", file);
            if (groupId) {
                formData.append("group_id", groupId);
            }
            const response = await fetch("/contacts/import/", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + accessToken
                },
                body: formData
            });
            const result = await response.json();
            if (response.ok) {
                successElement.textContent =
                    `Импорт завершён. Добавлено контактов: ${result.created || 0}`;
                successElement.classList.remove("d-none");
            } else {
                errorElement.textContent =
                    result.detail || "Не удалось импортировать контакты";
                errorElement.classList.remove("d-none");
            }
        });
});