const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    addMessage(message, "user-message");
    chatInput.value = "";

    const res = await fetch("/send_message", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });
    const data = await res.json();
    addMessage(data.reply, "decken-message");
    chatBox.scrollTop = chatBox.scrollHeight;
});

function addMessage(text, className) {
    const msgDiv = document.createElement("div");
    msgDiv.className = className;
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
