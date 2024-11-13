function debug(websocket) {
    websocket.addEventListener("open", () => {
        console.log("Connected to WebSocket server");
    });

    websocket.addEventListener("close", () => {
        console.log("Disconnected from WebSocket server");
    });

    websocket.addEventListener("error", (error) => {
        console.error("WebSocket error:", error);
    });
}


function listenMessageWS(chatWindow, websocket) {
    // Listen for incoming messages
    websocket.addEventListener("message", ({ data }) => {
        console.log("Incoming message:", data);  // Debugging line
        const event = JSON.parse(data);
        if (event.type === "message") {
            const messageElement = document.createElement("div");
            messageElement.textContent = `${event.username}: ${event.text}`;
            chatWindow.appendChild(messageElement);
            chatWindow.scrollTop = chatWindow.scrollHeight;  // Scroll to bottom
        }
    });

}

function sendMessageWS(messageInput,sendButton, username, websocket) {
    // Send message on button click
    sendButton.addEventListener("click", () => {
        const text = messageInput.value;
        if (text && websocket.readyState === WebSocket.OPEN) {  // Ensure WebSocket is open
            const message = {
                type: "message",
                username: username,
                text: text
            };
            websocket.send(JSON.stringify(message));
            messageInput.value = "";
        } else {
            console.warn("WebSocket is not open. Cannot send message.");
        }
    });
}


window.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const username = "User" + Math.floor(Math.random() * 1000);

    const websocket = new WebSocket("ws://localhost:8001/");

    debug(websocket)
    listenMessageWS(chatWindow, websocket)
    sendMessageWS(messageInput, sendButton, username, websocket)

});
