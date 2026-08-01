const templateId = document.getElementById("template-id").value;
document.addEventListener("DOMContentLoaded",loadTemplate);
async function loadTemplate() {
    const response = await fetch(`/messages/${templateId}/`,
        {
            headers: {
                "Authorization":
                    "Bearer " + localStorage.getItem("access")
            }
        }
    );
    const template = await response.json();
    document.getElementById("title").value = template.title;
    document.getElementById("subject").value = template.subject;
    document.getElementById("body").value = template.body;
}
async function updateTemplate() {
    const response = await fetch(`/messages/${templateId}/update/`,
        {
            method: "PATCH",
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
        document.getElementById("error").innerText = "Ошибка сохранения";
    }
}