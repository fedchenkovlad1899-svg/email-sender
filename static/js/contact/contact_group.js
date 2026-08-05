document.addEventListener("DOMContentLoaded", async function () {
    const response = await fetch("/groups/", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("access")
        }
    });
    if (!response.ok) {
        document.getElementById("group-error").textContent = "Не удалось загрузить группы";
        document.getElementById("group-error").classList.remove("d-none");
        return;
    }
    const data = await response.json();
    const groups = data.results || data;
    const groupList = document.getElementById("group-list");
    groups.forEach(function (group) {
        groupList.innerHTML += `
            <tr>
                <td>${group.title}</td>
                <td>${group.contacts.length}</td>
                <td>
                    <a href="/email_sender/contact/group/${group.id}/update"class="btn btn-sm btn-primary">Изменить</a>
                    <button class="btn btn-sm btn-danger"onclick="deleteGroup(${group.id})">Удалить</button>
                </td>
            </tr>
        `;
    });
});

async function deleteGroup(groupId) {
    if (!confirm("Удалить группу?")) {
        return;
    }
    const response = await fetch(`/groups/${groupId}/delete/`,
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
        alert("Не удалось удалить группу");
    }
}