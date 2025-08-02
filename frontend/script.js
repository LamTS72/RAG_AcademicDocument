const chatBox = document.getElementById('chat-box');
const userInputField = document.getElementById('user-input-field');
const sendButton = document.getElementById('send-button');

userInputField.addEventListener('input', () => {
    userInputField.style.height = 'auto';
    userInputField.style.height = userInputField.scrollHeight + 'px';
});

sendButton.addEventListener('click', sendMessage);
userInputField.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = userInputField.value;
    if (userInput.trim() !== '') {
        addMessage(userInput, 'user');
        userInputField.value = '';
        showLoader();
        fetchAnswer(userInput);
    }
}

function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender + '-message');
    const p = document.createElement('p');
    p.textContent = message;
    messageElement.appendChild(p);

    if (sender === 'bot') {
        const copyButton = document.createElement('button');
        copyButton.textContent = 'Copy';
        copyButton.classList.add('copy-button');
        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(message);
        });
        messageElement.appendChild(copyButton);
    }

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showLoader() {
    const loaderElement = document.createElement('div');
    loaderElement.classList.add('message', 'bot-message');
    loaderElement.id = 'loader';
    const loader = document.createElement('div');
    loader.classList.add('loader');
    loaderElement.appendChild(loader);
    chatBox.appendChild(loaderElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.remove();
    }
}

async function fetchAnswer(userInput) {
    try {
        const response = await fetch('http://localhost:8000/generative_ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userInput })
        });

        hideLoader();

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        addMessage(data.answer, 'bot');
    } catch (error) {
        hideLoader();
        console.error('There was a problem with the fetch operation:', error);
        addMessage('Sorry, something went wrong. Please try again.', 'bot');
    }
}

window.onload = function() {
  addMessage("Hello! How can I help you today?", "bot");
};
