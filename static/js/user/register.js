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
    const form = document.getElementById("registerForm");

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/register/", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        const message = document.getElementById("message");

        if (response.ok) {
            message.innerHTML =
                '<div class="alert alert-success">Регистрация прошла успешно</div>';

            form.reset();
        } else {
            message.innerHTML =
                '<div class="alert alert-danger">' +
                JSON.stringify(data) +
                '</div>';
        }
    });