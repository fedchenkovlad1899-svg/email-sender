document.addEventListener("DOMContentLoaded", loadCampaigns);
async function loadCampaigns() {
    const response = await fetch("/campaigns/", {
        headers: {
            "Authorization":
                "Bearer " + localStorage.getItem("access")
        }
    });

    if (!response.ok) {
        showError("Не удалось загрузить рассылки");
        return;
    }

    const data = await response.json();
    const campaigns = data.results || data;
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