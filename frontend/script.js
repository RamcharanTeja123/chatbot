async function sendMessage() {

    const input = document.querySelector(".chat-input input");
    const message = input.value.trim();

    if (message === "") {
        return;
    }

    const chatBox = document.getElementById("chat-box");

    // Show user message
    chatBox.innerHTML += `<p>You: ${message}</p>`;

    input.value = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Show bot response
        chatBox.innerHTML += `<p>Bot: ${data.reply}</p>`;

    } catch (error) {

        console.error("Error:", error);

        chatBox.innerHTML += `
            <p>Bot: Sorry, something went wrong.</p>
        `;
    }
}