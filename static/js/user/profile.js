async function refreshAccessToken() {
        const refreshToken = localStorage.getItem("refresh");
        if (!refreshToken) {
            return null;
        }
        const response = await fetch("/token/refresh/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });

        if (!response.ok) {
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            return null;
        }

        const data = await response.json();
        localStorage.setItem("access", data.access);
        return data.access;
    }

    async function getProfile(accessToken) {
        return fetch("/profile/", {
            method: "GET",
            headers: {"Authorization": "Bearer " + accessToken}
        });
    }

    document.addEventListener("DOMContentLoaded", async function () {
        let accessToken = localStorage.getItem("access");
        const contentElement = document.getElementById("profile-content");
        const errorElement = document.getElementById("profile-error");
        if (!accessToken) {
            window.location.href = "/email_sender/login/";
            return;
        }
        try {
            let response = await getProfile(accessToken);
            if (response.status === 401) {
                accessToken = await refreshAccessToken();
                if (!accessToken) {
                    window.location.href = "/email_sender/login/";
                    return;
                }
                response = await getProfile(accessToken);
            }
            if (!response.ok) {
                throw new Error("Не удалось получить данные профиля");
            }
            const user = await response.json();
            document.getElementById("profile-username").textContent = user.username || "Не указано";
            document.getElementById("profile-email").textContent = user.email || "Не указано";
            document.getElementById("profile-first-name").textContent = user.first_name || "Не указано";
            document.getElementById("profile-last-name").textContent = user.last_name || "Не указано";
            document.getElementById("profile-role").textContent = user.role || "Пользователь";
            document.getElementById("profile-status").textContent = user.is_active ? "Активен" : "Заблокирован";
            document.getElementById("profile-date-joined").textContent = user.date_joined ? new Date(user.date_joined).toLocaleString("ru-RU") : "Нет данных";
            contentElement.classList.remove("d-none");

        } catch (error) {
            errorElement.textContent = error.message;
            errorElement.classList.remove("d-none");
        }
    });