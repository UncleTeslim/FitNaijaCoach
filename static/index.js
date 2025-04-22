function getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
  
  function appendMessage(content, sender) {
    const chatBox = document.getElementById("chat");
    const messageClass = sender === "user" ? "user" : "bot";
    const label = sender === "user" ? "You" : "Coach";
  
    const formattedContent = sender === "bot" ? marked.parse(content) : content;
    const timestamp = getTimestamp();
  
    // Add timestamp inside the same div as the message content
    const messageDiv = `
      <div class='message ${messageClass}'>
        <strong>${label}:</strong><br>
        ${formattedContent}
        <div class='timestamp'>${timestamp}</div>
      </div>`;
  
    chatBox.innerHTML += messageDiv;
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  
  async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const userMessage = inputField.value.trim();
    if (!userMessage) return;
  
    appendMessage(userMessage, "user");
    inputField.value = "";
  
    const loading = document.getElementById("loading");
    loading.style.display = "block";
  
    try {
      const response = await fetch("/get_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
  
      const data = await response.json();
      appendMessage(data.response, "bot");
    } catch (error) {
      appendMessage("Something went wrong. Please try again.", "bot");
      console.error("Error:", error);
    } finally {
      loading.style.display = "none";
    }
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("userInput");
    inputField.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });
  });
  
  