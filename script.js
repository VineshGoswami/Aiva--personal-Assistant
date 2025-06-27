function sendCommand() {
    let userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    document.getElementById("user-input").value = "";

    fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>AIVA:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function startListening() {
    fetch("/listen", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        document.getElementById("chat-box").innerHTML += `<p><strong>You:</strong> ${data.command}</p>`;
        document.getElementById("chat-box").innerHTML += `<p><strong>AIVA:</strong> ${data.response}</p>`;
    });
}
