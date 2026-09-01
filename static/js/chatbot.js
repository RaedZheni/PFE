function toggleChat() {
    const box = document.getElementById("chatbot-box");
    box.classList.toggle("open");
}

async function getContext() {
    try {
        const res = await fetch("/api/context");
        const data = await res.json();
        return JSON.stringify(data);
    } catch {
        return "No data available.";
    }
}

async function sendMessage() {
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");
    const text = input.value.trim();
    if (!text) return;

    const userMsg = document.createElement("div");
    userMsg.className = "user-msg";
    userMsg.textContent = text;
    messages.appendChild(userMsg);
    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    const typing = document.createElement("div");
    typing.className = "bot-msg";
    typing.textContent = "...";
    messages.appendChild(typing);
    messages.scrollTop = messages.scrollHeight;

    const context = await getContext();

    try {
        const response = await fetch("https://api.anthropic.com/v1/messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "anthropic-dangerous-direct-browser-access": "true"
            },
            body: JSON.stringify({
                model: "claude-sonnet-4-6",
                max_tokens: 300,
                system: `You are RaedAI, the smart assistant of this HR management app.
You have full access to the company data below. Use it to answer questions.
Never say you don't have access to data.
Keep answers short, 2-3 lines max, no bullet points, no markdown.
Only answer HR-related questions about employees, contracts, projects, and departments.
If asked something outside HR, say: "I'm RaedAI, I only assist with HR topics."

Company data:
${context}`,
                messages: [{ role: "user", content: text }]
            })
        });

        const data = await response.json();
        typing.textContent = data.content[0].text;
    } catch {
        typing.textContent = "Something went wrong. Please try again.";
    }

    messages.scrollTop = messages.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("chatbot-input");
    if (input) {
        input.addEventListener("keydown", function (e) {
            if (e.key === "Enter") sendMessage();
        });
    }
});