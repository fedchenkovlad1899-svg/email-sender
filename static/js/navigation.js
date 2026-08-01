document.addEventListener("DOMContentLoaded", function() {
        const accessToken = localStorage.getItem("access");

        const guestLinks = document.querySelectorAll(".guest-link");
        const userLinks = document.querySelectorAll(".user-link");

        if (accessToken) {
            showUserNavigation();

            loadCurrentUser(accessToken);
        } else {
            showGuestNavigation();
        }

        const logoutButton = document.getElementById("logout-button");

        if (logoutButton) {
            logoutButton.addEventListener("click", logoutUser);
        }
    });


    function showUserNavigation() {
        const guestLinks = document.querySelectorAll(".guest-link");
        const userLinks = document.querySelectorAll(".user-link");

        guestLinks.forEach(function(element) {
            element.classList.add("d-none");
        });

        userLinks.forEach(function(element) {
            element.classList.remove("d-none");
        });
    }


    function showGuestNavigation() {
        const guestLinks = document.querySelectorAll(".guest-link");
        const userLinks = document.querySelectorAll(".user-link");

        guestLinks.forEach(function(element) {
            element.classList.remove("d-none");
        });

        userLinks.forEach(function(element) {
            element.classList.add("d-none");
        });
    }


    async function loadCurrentUser(accessToken) {
        try {
            const response = await fetch("/profile/", {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + accessToken
                }
            });

            if (!response.ok) {
                const errorData = await response.json();

                console.error(
                    "Ошибка получения профиля:",
                    response.status,
                    errorData
                );

                return;
            }

            const user = await response.json();

            const navbarUsername =
                document.getElementById("navbar-username");

            if (navbarUsername) {
                navbarUsername.textContent =
                    user.username ||
                    user.email ||
                    "Пользователь";
            }

        } catch (error) {
            console.error(
                "Ошибка запроса профиля:",
                error
            );
        }
    }


    async function logoutUser() {
        const accessToken =
            localStorage.getItem("access");

        const refreshToken =
            localStorage.getItem("refresh");

        if (!accessToken || !refreshToken) {
            clearTokens();
            window.location.href = "/email_sender/home/";
            return;
        }

        try {
            const response = await fetch("/logout/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + accessToken
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            let data = {};

            try {
                data = await response.json();
            } catch (error) {
                data = {};
            }

            if (!response.ok) {
                console.error(
                    "Ошибка выхода:",
                    response.status,
                    data
                );

                alert(
                    data.detail ||
                    "Сервер не выполнил выход."
                );

                return;
            }

            clearTokens();

            window.location.href = "/email_sender/home/";

        } catch (error) {
            console.error(
                "Ошибка запроса выхода:",
                error
            );

            alert(
                "Не удалось отправить запрос выхода."
            );
        }
    }


    function clearTokens() {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
    }