const token = localStorage.getItem("access");

let previousUrl = null;
let nextUrl = null;
let currentPage = 1;


document.addEventListener("DOMContentLoaded", async function () {
    await loadStatistics();
    await loadLogs("/logs/");

    document.getElementById("previous-button").onclick = function () {
        if (previousUrl) {
            currentPage--;
            loadLogs(previousUrl);
        }
    };

    document.getElementById("next-button").onclick = function () {
        if (nextUrl) {
            currentPage++;
            loadLogs(nextUrl);
        }
    };
});


async function getData(url) {
    const response = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!response.ok) {
        throw new Error("Не удалось загрузить статистику");
    }

    return response.json();
}


async function loadStatistics() {
    try {
        const logs = [];
        let url = "/logs/";

        while (url) {
            const data = await getData(url);
            logs.push(...(data.results || data));
            url = data.next || null;
        }

        const campaigns = await getData(
            "/campaigns/?status=scheduled"
        );

        document.getElementById("total-count").textContent =
            logs.length;

        document.getElementById("sent-count").textContent =
            logs.filter(log => log.status === "sent").length;

        document.getElementById("failed-count").textContent =
            logs.filter(log => log.status === "failed").length;

        document.getElementById("pending-count").textContent =
            campaigns.count ?? (campaigns.results || campaigns).length;

    } catch (error) {
        showError(error.message);
    }
}


async function loadLogs(url) {
    try {
        const data = await getData(url);
        const logs = data.results || data;

        previousUrl = data.previous || null;
        nextUrl = data.next || null;

        const list = document.getElementById("logs-list");

        list.innerHTML = logs.length
            ? logs.map(log => `
                <tr>
                    <td>${log.campaign_title || "Не указано"}</td>
                    <td>${log.contact_email || "Не указано"}</td>
                    <td>${statusName(log.status)}</td>
                    <td>${log.error_message || "Нет"}</td>
                    <td>${
                        log.sent_at
                            ? new Date(log.sent_at).toLocaleString("ru-RU")
                            : "Не отправлено"
                    }</td>
                </tr>
            `).join("")
            : `
                <tr>
                    <td colspan="5" class="text-center">
                        История отправок пока отсутствует
                    </td>
                </tr>
            `;

        document.getElementById("previous-button").disabled =
            !previousUrl;

        document.getElementById("next-button").disabled =
            !nextUrl;

        const total = data.count ?? logs.length;
        const pages = Math.max(1, Math.ceil(total / 20));

        document.getElementById("page-info").textContent =
            `Страница ${currentPage} из ${pages}`;

    } catch (error) {
        showError(error.message);
    }
}


function statusName(status) {
    return {
        pending: "Ожидает отправки",
        sent: "Отправлено",
        failed: "Ошибка"
    }[status] || status;
}


function showError(message) {
    const element = document.getElementById("statistic-error");

    element.textContent = message;
    element.classList.remove("d-none");
}