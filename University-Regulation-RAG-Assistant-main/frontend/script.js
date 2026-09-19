const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");


async function askQuestion() {

    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }


    // Display user's question
    const userMessage = document.createElement("div");

    userMessage.className = "message user-message";
    userMessage.textContent = question;

    chatBox.appendChild(userMessage);


    // Clear input
    questionInput.value = "";


    // Show loading message
    const loadingMessage = document.createElement("div");
loadingMessage.className = "message bot-message thinking-message";

loadingMessage.innerHTML = `
    Thinking
    <span class="thinking-dot"></span>
    <span class="thinking-dot"></span>
    <span class="thinking-dot"></span>
`;

chatBox.appendChild(loadingMessage);

    try {

        // Send question to FastAPI
        const response = await fetch("http://127.0.0.1:8000/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        // Remove loading message
        loadingMessage.remove();


        // Create answer message
        const botMessage = document.createElement("div");

        botMessage.className = "message bot-message";


        // Display answer
        botMessage.innerHTML = `
    <strong>Answer:</strong><br>
    ${data.answer}

    <div class="source-section">
        <div class="source-title">📚 Sources</div>

        ${data.sources.map(source => `
            <div class="source-item">
                📄 ${source.document}<br>
                📖 Page ${source.page}
            </div>
        `).join("")}
    </div>
`;


        chatBox.appendChild(botMessage);


    } catch (error) {

        loadingMessage.textContent =
            "Sorry, I could not connect to the server.";

        console.error(error);

    }


    // Scroll to latest message
    chatBox.scrollTop = chatBox.scrollHeight;
}


// Send button
sendButton.addEventListener("click", askQuestion);


// Press Enter to send
questionInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});
const suggestionButtons = document.querySelectorAll(".suggestion-button");

suggestionButtons.forEach(function(button) {
    button.addEventListener("click", function() {

        questionInput.value = button.textContent.trim();

        askQuestion();

    });
});
const clearButton = document.getElementById("clear-button");

clearButton.addEventListener("click", function() {
    chatBox.innerHTML = `
        <div class="message bot-message welcome-message">
            <strong>Welcome to Vignan University Regulation Assistant 👋</strong>
            <br><br>

            I can help you find information from the
            university regulations.
            <br><br>

            You can ask about attendance, examinations,
            grading, credits, branch change, degree requirements,
            and other academic regulations.
            <br><br>

            How can I help you?
        </div>

        <div class="suggested-questions">

            <p>Try asking:</p>

            <button class="suggestion-button">
                What is the minimum attendance requirement?
            </button>

            <button class="suggestion-button">
                How is SGPA calculated?
            </button>

            <button class="suggestion-button">
                What are the rules for supplementary examinations?
            </button>

            <button class="suggestion-button">
                How can I change my branch?
            </button>

        </div>
    `;

    // Reconnect suggested-question buttons after clearing
    const newSuggestionButtons =
        document.querySelectorAll(".suggestion-button");

    newSuggestionButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            questionInput.value = button.textContent.trim();
            askQuestion();
        });
    });
});