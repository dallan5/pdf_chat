window.onbeforeunload = function() {
    navigator.sendBeacon('/clear_session');
};

let latestSelectedText = "";

document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    const chatWindow = document.getElementById("chat-window");
    const userMessage = document.createElement("div");
    userMessage.className = "user";
    userMessage.textContent = formObject.query;
    chatWindow.appendChild(userMessage);

    // Clear the input field
    event.target.query.value = '';  // This line clears the input field

    fetch("/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
    })
        .then(response => response.json())
        .then(data => {
            const aiMessage = document.createElement("div");
            aiMessage.className = data.role || "assistant";
            aiMessage.innerHTML = data.message;
            chatWindow.appendChild(aiMessage);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        })
        .catch(error => {
            console.error("Error:", error);
        });
});
