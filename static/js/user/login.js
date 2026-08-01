
    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {
                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }

    const csrftoken = getCookie("csrftoken");

    const form = document.getElementById("loginForm");
    const message = document.getElementById("message");

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/login/", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);


            window.location.href = "/email_sender/home/";
        } else {
            message.innerHTML =
                '<div class="alert alert-danger">' +
                JSON.stringify(data) +
                '</div>';
        }
    });