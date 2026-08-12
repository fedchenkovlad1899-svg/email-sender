const token = localStorage.getItem("access");

let previousUrl = null;
let nextUrl = null;
let currentPage = 1;

document.addEventListener("DOMContentLoaded", function (){loadCampaigns("/campaigns/?ordering=-created_at");
document.getElementById("search-button")
        .addEventListener("click", function () {
            currentPage = 1;
            loadFilteredCampaigns();
        });


    document.getElementById("reset-button").addEventListener("click", function () {
            document.getElementById("search-input").value = "";
            document.getElementById("status-filter").value = "";
            document.getElementById("ordering").value = "-created_at";
            currentPage = 1;
            loadCampaigns("/campaigns/?ordering=-created_at");
        });

    document.getElementById("previous-button").addEventListener("click", function () {
            if (previousUrl) {
                currentPage--;
                loadCampaigns(previousUrl);
            }
        });

    document.getElementById("next-button").addEventListener("click", function () {
            if (nextUrl) {
                currentPage++;
                loadCampaigns(nextUrl);
            }
        });
});



function loadFilteredCampaigns() {
    const search = document.getElementById("search-input").value.trim();
    const status = document.getElementById("status-filter").value;
    const ordering = document.getElementById("ordering").value;
    const params = new URLSearchParams();
    if (search) {
        params.append("search", search);
    }
    if (status) {
        params.append("status", status);
    }
    if (ordering) {
        params.append("ordering", ordering);
    }
    loadCampaigns("/campaigns/?" + params.toString());
}
async function loadCampaigns(url) {
    const response = await fetch(url, {
        headers: {
            "Authorization":
                "Bearer " + token
        }
    });

    if (!response.ok) {
        showError("Не удалось загрузить рассылки");
        return;
    }

    const data = await response.json();
    const campaigns = data.results || data;
    previousUrl = data.previous || null;
    nextUrl = data.next || null;
    const campaignList = document.getElementById("campaign-list");

    campaignList.innerHTML = "";

    campaigns.forEach(function (campaign) {
        const canEdit = [
            "draft",
            "scheduled"
        ].includes(campaign.status);

        const canSend = [
            "draft",
            "scheduled",
            "failed"
        ].includes(campaign.status);

        const canCancel =
            campaign.status === "scheduled";

         const canDelete = [
            "draft",
            "canceled"
        ].includes(campaign.status);

        campaignList.innerHTML += `
            <tr>
                <td>${campaign.title}</td>

                <td>${getStatusName(campaign.status)}</td>

                <td>
                    ${
                        campaign.scheduled_at
                            ? new Date(
                                campaign.scheduled_at
                            ).toLocaleString("ru-RU")
                            : "Не запланировано"
                    }
                </td>

                <td>${campaign.sent_count || 0}</td>

                <td>${campaign.failed_count || 0}</td>

                <td>
                    ${
                        canEdit
                            ? `
                                <a href="/email_sender/campaign/${campaign.id}/update" class="btn btn-sm btn-primary">Изменить</a>
                            `
                            : ""
                    }

                    ${
                        canSend
                            ? `
                                <button
                                    type="button"
                                    class="btn btn-sm btn-success"
                                    onclick="sendCampaign(${campaign.id})"
                                >
                                    Отправить
                                </button>
                            `
                            : ""
                    }

                    ${
                        canCancel
                            ? `
                                <button
                                    type="button"
                                    class="btn btn-sm btn-warning"
                                    onclick="cancelCampaign(${campaign.id})"
                                >
                                    Отменить
                                </button>
                            `
                            : ""
                    }
                   ${
                        canDelete
                            ? `
                                <button
                                    type="button"
                                    class="btn btn-sm btn-danger"
                                    onclick="deleteCampaign(${campaign.id})"
                                >
                                    Удалить
                                </button>
                            `
                            : ""
                    }
                </td>
            </tr>
        `;
    });
    if (campaigns.length === 0) {
        campaignList.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    Рассылки не найдены
                </td>
            </tr>
        `;
    }
    document.getElementById("previous-button").disabled = !previousUrl;
    document.getElementById("next-button").disabled = !nextUrl;
    const total = data.count ?? campaigns.length;
    const totalPages = Math.max(1, Math.ceil(total / 20));
    document.getElementById("page-info").textContent = `Страница ${currentPage} из ${totalPages}`;

}


function getStatusName(status) {
    const statuses = {
        draft: "Черновик",
        scheduled: "Запланирована",
        processing: "Отправляется",
        completed: "Завершена",
        completed_with_errors: "Завершена с ошибками",
        failed: "Ошибка",
        canceled: "Отменена"
    };

    return statuses[status] || status;
}


async function sendCampaign(campaignId) {
    if (!confirm("Запустить рассылку?")) {
        return;
    }

    const response = await fetch(
        `/campaigns/${campaignId}/send/`,
        {
            method: "POST",
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("access")
            }
        }
    );

    if (response.ok) {
        window.location.reload();
        return;
    }

    const error = await response.json();

    alert(
        error.detail ||
        "Не удалось запустить рассылку"
    );
}


async function cancelCampaign(campaignId) {
    if (!confirm("Отменить запланированную рассылку?")) {
        return;
    }

    const response = await fetch(
        `/campaigns/${campaignId}/cancel/`,
        {
            method: "POST",
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("access")
            }
        }
    );

    if (response.ok) {
        window.location.reload();
        return;
    }

    const error = await response.json();

    alert(
        error.detail ||
        "Не удалось отменить рассылку"
    );
}


async function deleteCampaign(campaignId) {
    if (!confirm("Удалить рассылку?")) {
        return;
    }

    const response = await fetch(
        `/campaigns/${campaignId}/delete/`,
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
        return;
    }

    const error = await response.json();

    alert(
        error.detail ||
        "Не удалось удалить рассылку"
    );
}


function showError(message) {
    const errorElement =
        document.getElementById("campaign-error");

    errorElement.textContent = message;
    errorElement.classList.remove("d-none");
}