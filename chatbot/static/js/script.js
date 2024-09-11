document.getElementById('sendButton').addEventListener('click', function() {
    let userMessage = document.getElementById('userInput').value;

    fetch('/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        let chatBox = document.getElementById('chatBox');
        chatBox.innerHTML += `<div>User: ${userMessage}</div>`;
        chatBox.innerHTML += `<div>Bot: ${data.response}</div>`;
        document.getElementById('userInput').value = ''; // เคลียร์ช่องข้อความ
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
