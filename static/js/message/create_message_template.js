async function createTemplate() {

    const response = await fetch("/messages/create/",
        {
            method: "POST",
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("access"),
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                title: document.getElementById("title").value,
                subject: document.getElementById("subject").value,
                body: document.getElementById("body").value
            })
        }
    );

    if (response.ok) {
        window.location.href = "/email_sender/message_template/";
    } else {
        document.getElementById("error").classList.remove("d-none");
        document.getElementById("error").innerText = "Ошибка создания шаблона";
    }
}